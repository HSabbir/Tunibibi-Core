from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from system.models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.conf import settings
import os
import requests
import json
from django.db.models import Q
from django.conf import settings


def seed():
    if not User.objects.filter(email='support@tunibibi.com').exists():
        User.objects.create_superuser(
            first_name='Super',
            last_name='Admin',
            username='support@tunibibi.com',
            email='support@tunibibi.com',
            password='tuni@951753'
        )
    if Settings.objects.all().count() == 0:
        Settings.objects.create()
    if Legal.objects.all().count() == 0:
        Legal.objects.create()


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core.home'))

    # Data Seeding
    seed()

    login_form = LoginForm()
    if request.method == 'POST':
        try:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user_email = login_form.cleaned_data.get('email')
                user_password = login_form.cleaned_data.get('password')

                # Get the user instance
                user_instance = User.objects.filter(email=user_email)

                # Checking if the user exists
                if user_instance.exists():
                    if not user_instance[0].is_active:
                        messages.warning(request, 'You account is inactive.')
                        return HttpResponseRedirect(reverse('core.login'))

                    if not user_instance[0].is_superuser or not user_instance[0].is_staff:
                        messages.warning(request, 'You are not authorised to login.')
                        return HttpResponseRedirect(reverse('core.login'))
                    # Get the username
                    username = user_instance[0].username

                    # Check if the user is valid
                    valid_user = authenticate(request, username=username, password=user_password)

                    if valid_user is not None:
                        # Generating login session
                        auth_login(request, valid_user)

                        return HttpResponseRedirect(reverse('core.home'))
                    else:
                        # Passing the error message
                        messages.error(request, 'Invalid email address or password.')
                else:
                    # Passing the error message
                    messages.error(request, 'No user found with the provided email address.')
        except Exception as e:
            messages.error(request, e)
    context = {
        'login_form': login_form
    }
    return render(request, 'core/auth-login.html', context)


@login_required(login_url='core.login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('core.login'))


@login_required(login_url='core.login')
def home(request):
    context = {}
    return render(request, 'core/home.html', context)


@login_required(login_url='core.login')
def editProfile(request):
    user_change_form = ProfileEditForm(instance=request.user)
    if request.method == 'POST':
        try:
            user_change_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
            if user_change_form.is_valid():
                user_change_form.save()
                if 'profile_photo' in user_change_form.changed_data:
                    if UserPhoto.objects.filter(user=request.user).exists():
                        photo_instance = UserPhoto.objects.get(user=request.user)
                        try:
                            photo_path = os.path.join(settings.BASE_DIR, photo_instance.profile_photo.path)
                            if os.path.exists(photo_path):
                                os.remove(photo_path)
                        except Exception:
                            pass
                        photo_instance.profile_photo = request.FILES['profile_photo']
                        photo_instance.save()
                    else:
                        UserPhoto.objects.create(
                            user=request.user,
                            profile_photo=request.FILES['profile_photo']
                        )
                messages.success(request, 'Profile updated successfully.')
                return HttpResponseRedirect(reverse('core.edit.profile'))
        except Exception as e:
            messages.error(request, e)
    context = {
        'title': 'Edit Profile',
        'user_change_form': user_change_form
    }
    return render(request, 'core/edit-profile.html', context)


@login_required(login_url='core.login')
def changePassword(request):
    change_password_form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        try:
            change_password_form = ChangePasswordForm(request.user, request.POST)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)
                messages.add_message(request, messages.SUCCESS, 'Your password has been updated!')
                return HttpResponseRedirect(reverse('core.change.password'))
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
    context = {
        'title': 'Change Password',
        'change_password_form': change_password_form
    }
    return render(request, 'core/change-password.html', context)


@login_required(login_url='core.login')
def changeUserPassword(request):
    if request.user.is_superuser:
        try:
            if request.method == 'POST':
                email = request.POST['email_cp']
                password = request.POST['password_cp']
                User.objects.filter(email=email).update(password=make_password(password))
                messages.success(request, 'User password changed successfully.')
            else:
                return HttpResponseRedirect(reverse('core.administrators'))
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(reverse('core.administrators'))
    else:
        return HttpResponseRedirect(reverse('core.home'))


@login_required(login_url='core.login')
def administrators(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('core.home'))
    add_admin_form = AdminCreate()
    if request.method == 'POST':
        try:
            add_admin_form = AdminCreate(request.POST)
            if add_admin_form.is_valid():
                name = add_admin_form.cleaned_data.get('name')
                email = add_admin_form.cleaned_data.get('email')
                password = add_admin_form.cleaned_data.get('password')

                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Another user already exists with this email.')
                else:
                    User.objects.create_user(
                        first_name=name,
                        username=email,
                        email=email,
                        password=password,
                        is_staff=True
                    )
                    messages.success(request, 'Administrator added successfully.')
                    return HttpResponseRedirect(reverse('core.administrators'))
        except Exception as e:
            messages.error(request, e)
    admin_list = User.objects.all()
    context = {
        'title': 'Administrators',
        'admin_list': admin_list,
        'add_admin_form': add_admin_form
    }
    return render(request, 'core/admin-list.html', context)


@login_required(login_url='core.login')
def administratorBan(request, user_id):
    if request.user.is_superuser and request.user.id != user_id:
        try:
            User.objects.filter(id=user_id).update(is_active=False)
            messages.success(request, 'Administrator banned successfully.')
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(reverse('core.administrators'))
    else:
        return HttpResponseRedirect(reverse('core.home'))


@login_required(login_url='core.login')
def administratorUnban(request, user_id):
    if request.user.is_superuser and request.user.id != user_id:
        try:
            User.objects.filter(id=user_id).update(is_active=True)
            messages.success(request, 'Administrator unbanned successfully.')
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(reverse('core.administrators'))
    else:
        return HttpResponseRedirect(reverse('core.home'))


@login_required(login_url='core.login')
def administratorDelete(request, user_id):
    if request.user.is_superuser and request.user.id != user_id:
        try:
            User.objects.get(id=user_id).delete()
            messages.success(request, 'Administrator deleted successfully.')
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(reverse('core.administrators'))
    else:
        return HttpResponseRedirect(reverse('core.home'))


@login_required(login_url='core.login')
def systemSettings(request):
    if request.user.is_superuser:
        system_instance = Settings.objects.all().last()
        system_settings = SystemSettingsForm(instance=system_instance)
        if request.method == 'POST':
            try:
                system_settings = SystemSettingsForm(instance=system_instance, data=request.POST, files=request.FILES)
                if system_settings.is_valid():
                    system_settings.save()
                    messages.success(request, 'System settings updated successfully.')
                    return HttpResponseRedirect(reverse('core.system.settings'))
            except Exception as e:
                messages.error(request, e)
        context = {
            'title': 'System Settings',
            'system_settings': system_settings
        }
        return render(request, 'core/system_settings.html', context)
    else:
        return HttpResponseRedirect(reverse('core.home'))


@login_required(login_url='core.login')
def legal(request, doc_name):
    legal_instance = Legal.objects.all().last()
    if doc_name == 'faq':
        legal_form = FAQForm(instance=legal_instance)
        title = 'FAQ'
    elif doc_name == 'policy':
        legal_form = PolicyForm(instance=legal_instance)
        title = 'Policy'
    else:
        legal_form = TermsForm(instance=legal_instance)
        title = 'Terms & Conditions'
    if request.method == 'POST':
        try:
            if doc_name == 'faq':
                legal_form = FAQForm(instance=legal_instance, data=request.POST)
            elif doc_name == 'policy':
                legal_form = PolicyForm(instance=legal_instance, data=request.POST)
            else:
                legal_form = TermsForm(instance=legal_instance, data=request.POST)
            if legal_form.is_valid():
                legal_form.save()
                messages.success(request, 'Legal data updated successfully.')
                return HttpResponseRedirect(reverse('core.legal', kwargs={'doc_name': doc_name}))
        except Exception as e:
            messages.error(request, e)
    context = {
        'title': title,
        'legal_form': legal_form
    }
    return render(request, 'core/legal.html', context)


@login_required(login_url='core.login')
def country(request):
    if 'reload' in request.GET and request.GET['reload']:
        try:
            url = "https://countriesnow.space/api/v0.1/countries/flag/images"
            response = requests.request("GET", url, headers={}, data={})
            response = json.loads(response.text)
            if not response['error']:
                for data in response['data']:
                    if Country.objects.filter(name=data['name']).exists():
                        country_instance = Country.objects.get(name=data['name'])
                        country_instance.flag = data['flag']
                        country_instance.save()
                    else:
                        Country.objects.create(
                            name=data['name'],
                            flag=data['flag']
                        )
                return HttpResponseRedirect(reverse('core.country'))
            else:
                messages.error(request, response['msg'])
        except Exception as e:
            messages.error(request, e)
    country_list = Country.objects.all().order_by('name')
    context = {
        'title': 'Country',
        'country_list': country_list
    }
    return render(request, 'core/country-list.html', context)


@login_required(login_url='core.login')
def countryToggle(request, country_id):
    try:
        country_instance = Country.objects.get(id=country_id)
        country_instance.status = not country_instance.status
        country_instance.save()
        messages.success(request, 'Country status updated successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.country'))


@login_required(login_url='core.login')
def countryDelete(request, country_id):
    try:
        Country.objects.get(id=country_id).delete()
        messages.success(request, 'Country deleted successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.country'))


@login_required(login_url='core.login')
def city(request):
    city_list = []
    if 'reload' in request.GET and request.GET['reload']:
        try:
            url = "https://countriesnow.space/api/v0.1/countries/states"
            response = requests.request("GET", url, headers={}, data={})
            response = json.loads(response.text)
            if not response['error']:
                City.objects.all().delete()
                for data in response['data']:
                    if Country.objects.filter(name=data['name']).exists():
                        try:
                            country_instance = Country.objects.get(name=data['name'])
                            for c in data['states']:
                                City.objects.create(
                                    country=country_instance,
                                    name=c['name']
                                )
                        except Exception as e:
                            print(e)
                            pass
                return HttpResponseRedirect(reverse('core.city'))
            else:
                messages.error(request, response['msg'])
        except Exception as e:
            messages.error(request, e)
    if 'country' in request.GET:
        try:
            city_list = City.objects.filter(country_id=request.GET['country'])
        except Exception as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('core.city'))
    context = {
        'title': 'State',
        'city_list': city_list,
        'country_list': Country.objects.all().order_by('name')
    }
    return render(request, 'core/city-list.html', context)


@login_required(login_url='core.login')
def cityStatus(request):
    try:
        if 'country' in request.GET and 'status' in request.GET and 'city' in request.GET:
            if request.GET['city'] == 'all':
                City.objects.filter(country_id=request.GET['country']).update(status=request.GET['status'])
            else:
                City.objects.filter(country_id=request.GET['country'], id=request.GET['city']).update(
                    status=request.GET['status'])
            return HttpResponseRedirect(reverse('core.city') + '?country=' + request.GET['country'])
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.city'))


@login_required(login_url='core.login')
def cityDelete(request, city_id):
    try:
        City.objects.get(id=city_id, country_id=request.GET['country']).delete()
        messages.success(request, 'City deleted successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.city') + '?country=' + str(request.GET['country']))


@login_required(login_url='core.login')
def category(request):
    category_form = CategoryForm()
    if request.method == 'POST':
        try:
            category_form = CategoryForm(request.POST, request.FILES)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Category added successfully.')
                return HttpResponseRedirect(reverse('core.category'))
        except Exception as e:
            messages.error(request, e)
    category_list = Category.objects.all().order_by('order_sequence')
    context = {
        'title': 'Category List',
        'category_list': category_list,
        'category_form': category_form
    }
    return render(request, 'core/category-list.html', context)


@login_required(login_url='core.login')
def categoryEdit(request):
    category_id = request.GET['category']
    category_form = CategoryForm(instance=Category.objects.get(id=category_id))
    if request.method == 'POST':
        try:
            category_form = CategoryForm(data=request.POST, files=request.FILES,
                                         instance=Category.objects.get(id=category_id))
            if category_form.is_valid():
                if Category.objects.filter(id=category_form.cleaned_data.get('parent_category')).exists():
                    category_form.save()
                    messages.success(request, 'Category updated successfully.')
                    return HttpResponseRedirect(reverse('core.category'))
                else:
                    messages.error(request, 'Invalid parent category.')
        except Exception as e:
            messages.error(request, e)
    category_list = Category.objects.filter(~Q(id=category_id)).order_by('order_sequence')
    context = {
        'title': 'Edit Category',
        'category_list': category_list,
        'category_form': category_form
    }
    return render(request, 'core/category-list.html', context)


@login_required(login_url='core.login')
def categorySequence(request):
    try:
        if 'category' in request.GET and 'order' in request.GET:
            Category.objects.filter(id=request.GET['category']).update(order_sequence=request.GET['order'])
            messages.success(request, 'Category sequence updated successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.category'))


@login_required(login_url='core.login')
def categoryStatus(request, category_id):
    try:
        Category.objects.filter(id=category_id).update(status=request.GET['status'])
        messages.success(request, 'Category status updated successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.category'))


@login_required(login_url='core.login')
def categoryDelete(request, category_id):
    try:
        category_instance = Category.objects.get(id=category_id)
        image_path = category_instance.image.path
        if os.path.exists(os.path.join(settings.BASE_DIR, image_path)):
            os.remove(os.path.join(settings.BASE_DIR, image_path))
        messages.success(request, 'Category deleted successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.category'))


@login_required(login_url='core.login')
def sellerList(request):
    seller_list = Seller.objects.all()
    context = {
        'title': 'Seller List',
        'seller_list': seller_list
    }
    return render(request, 'core/seller-list.html', context)


@login_required(login_url='core.login')
def sellerBan(request, seller_id):
    if request.method == 'GET':
        try:
            seller_instance = Seller.objects.get(id=seller_id)
            seller_instance.seller_status = False
            seller_instance.user.is_active = False
            seller_instance.user.save()
            seller_instance.save()
            messages.success(request, 'Seller banned successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.seller.list'))


@login_required(login_url='core.login')
def sellerUnban(request, seller_id):
    if request.method == 'GET':
        try:
            seller_instance = Seller.objects.get(id=seller_id)
            seller_instance.seller_status = True
            seller_instance.user.is_active = True
            seller_instance.user.save()
            seller_instance.save()
            messages.success(request, 'Seller unbanned successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.seller.list'))


@login_required(login_url='core.login')
def sellerDelete(request, seller_id):
    if request.method == 'GET':
        try:
            seller_instance = Seller.objects.get(id=seller_id)
            seller_instance.user.delete()
            seller_instance.delete()
            messages.success(request, 'Seller deleted successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.seller.list'))


@login_required(login_url='core.login')
def userList(request):
    user_list = Users.objects.all()
    context = {
        'title': 'Users List',
        'user_list': user_list
    }
    return render(request, 'core/user-list.html', context)


@login_required(login_url='core.login')
def userBan(request, user_id):
    if request.method == 'GET':
        try:
            user_instance = Users.objects.get(id=user_id)
            user_instance.user_status = False
            user_instance.user.is_active = False
            user_instance.user.save()
            user_instance.save()
            messages.success(request, 'User banned successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.user.list'))


@login_required(login_url='core.login')
def userUnban(request, user_id):
    if request.method == 'GET':
        try:
            user_instance = Users.objects.get(id=user_id)
            user_instance.user_status = True
            user_instance.user.is_active = True
            user_instance.user.save()
            user_instance.save()
            messages.success(request, 'User unbanned successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.user.list'))


@login_required(login_url='core.login')
def userDelete(request, user_id):
    if request.method == 'GET':
        try:
            user_instance = Users.objects.get(id=user_id)
            user_instance.user.delete()
            user_instance.delete()
            messages.success(request, 'User deleted successfully.')
        except Exception as e:
            messages.error(request, e)
    return HttpResponseRedirect(reverse('core.user.list'))


@login_required(login_url='core.login')
def liveSchedule(request):
    live_list = LiveStreaming.objects.all().order_by('-end_datetime')
    context = {
        'title': 'Live Schedule',
        'live_list': live_list
    }
    return render(request, 'core/live-schedule.html', context)


@login_required(login_url='core.login')
def liveScheduleDelete(request, live_id):
    try:
        LiveStreaming.objects.get(id=live_id).delete()
        LiveStreamStatistics.objects.get(id=live_id).delete()
        messages.success(request, 'Live schedule deleted successfully.')
    except Exception as e:
        messages.error(request, e)
    return HttpResponseRedirect(reverse('core.live.schedule'))


@login_required(login_url='core.login')
def liveScheduleStatistics(request):
    live_list = LiveStreamStatistics.objects.all().order_by('-live__end_datetime')
    context = {
        'title': 'Live Statistics',
        'live_list': live_list
    }
    return render(request, 'core/live-statistics.html', context)
