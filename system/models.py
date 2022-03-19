from django.db import models
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import User
import uuid


def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "tunibibi_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class Settings(models.Model):
    app_name = models.CharField(max_length=200, default='Tunibibi')
    logo = models.ImageField(upload_to=generate_filename, default='default/600x200.png')
    favicon = models.ImageField(upload_to=generate_filename, default='default/favicon.ico')


class Country(models.Model):
    name = models.CharField(max_length=200)
    flag = models.URLField()
    status = models.BooleanField(default=False)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='city_country')
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)


class Seller(models.Model):
    STORE_CHOICE = (
        ('Retail', 'Retails'),
        ('Wholesale', 'Wholesale'),
        ('Both', 'Both')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='seller')
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='seller_country')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='seller_city')
    address = models.TextField()
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    store_type = models.CharField(max_length=200, choices=STORE_CHOICE)
    store_name = models.CharField(max_length=200)
    store_logo = models.ImageField(upload_to=generate_filename, default='default/default-logo.png')
    profile_photo = models.ImageField(upload_to=generate_filename, default='default/default-avatar.png')
    seller_status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user')
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='user_country')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='user_city')
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    entrepreneur = models.BooleanField(default=False)
    store_name = models.CharField(max_length=200, blank=True)
    profile_photo = models.ImageField(upload_to=generate_filename)
    user_status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=generate_filename)
    parent_category = models.IntegerField(default=0)
    order_sequence = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)


class LiveStreaming(models.Model):
    DURATION_CHOICES = (
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60, 60),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_stream', null=True)
    schedule_datetime = models.DateTimeField()
    duration = models.IntegerField(choices=DURATION_CHOICES)
    end_datetime = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='live_category')
    title = models.CharField(max_length=200)
    banner_image = models.ImageField(upload_to=generate_filename)
    created_on = models.DateTimeField(auto_now_add=True)


class LiveStreamStatistics(models.Model):
    live = models.ForeignKey(LiveStreaming, on_delete=models.CASCADE, related_name='live_stat')
    views = models.IntegerField()
    reaction = models.IntegerField()
    comments = models.IntegerField()
    updated_on = models.DateTimeField(auto_now_add=True)


class Legal(models.Model):
    faq = RichTextField()
    policy = RichTextField()
    terms_conditions = RichTextField()


class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to=generate_filename)


class DialCodes(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='dial_code')
    dial_code = models.CharField(max_length=10)
