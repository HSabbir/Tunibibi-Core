from django import forms
from system.models import *
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'john@example.com',
        'value': 'support@tunibibi.com'
    }), required=True, label='Email')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '********',
        'value': 'tuni@951753'
    }), required=True, label='Password')

    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. Alex'
    }), required=True, label='First Name')

    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. Smith'
    }), required=False, label='Last Name')

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. alex@example.com',
    }), required=False, disabled=True, label='Email Address')

    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'inputGroupFile01',
        'accept': '.jpg,.png'
    }), required=False, label='Profile Photo')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_photo']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }), required=True, label='Old Password')

    new_password1 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }), required=True, label='New Password')

    new_password2 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }), required=True, label='Confirm New Password')


class AdminCreate(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. Alex'
    }), required=True, label='Name')

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. alex@example.com',
    }), required=True, label='Email Address')

    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg ********'
    }), required=True, label='Password')

    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class SystemSettingsForm(forms.ModelForm):
    app_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. Tunibibi'
    }), required=True, label='App Name')

    logo = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'inputGroupFile01',
        'accept': '.jpg,.png,.svg'
    }), required=False, label='Logo', help_text='Recommended ratio 600x200')

    favicon = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'inputGroupFile02',
        'accept': '.jpg,.png,.svg'
    }), required=False, label='Favicon', help_text='Recommended ratio 256x256')

    class Meta:
        model = Settings
        fields = '__all__'


class FAQForm(forms.ModelForm):
    faq = forms.CharField(max_length=None, widget=CKEditorWidget(), required=True, label='')

    class Meta:
        model = Legal
        fields = ['faq']


class PolicyForm(forms.ModelForm):
    policy = forms.CharField(max_length=None, widget=CKEditorWidget(), required=True, label='')

    class Meta:
        model = Legal
        fields = ['policy']


class TermsForm(forms.ModelForm):
    terms_conditions = forms.CharField(max_length=None, widget=CKEditorWidget(), required=True, label='')

    class Meta:
        model = Legal
        fields = ['terms_conditions']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'eg. Grocery'
    }), required=True, label='Name')

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'inputGroupFile01',
        'accept': '.jpg,.png,.svg'
    }), required=True, label='Category Image')

    parent_category = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'value': 0,
        'hidden': True
    }), required=False, label='Parent Category')

    class Meta:
        model = Category
        fields = ['name', 'image', 'parent_category']
