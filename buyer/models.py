from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import seller.models

class BuyerInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_auth', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    photo = models.ImageField(default='default/default-logo.png',null=True,blank=True)
    city = models.TextField(null=True)
    postcode = models.TextField(null=True)
    reg_ip = models.GenericIPAddressField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)

class BuyerSgippingAddress(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_owner', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=20)
    street_address = models.TextField(null=True,blank=True)
    apt_suite_unit = models.TextField(null=True,blank=True)
    city = models.TextField(null=True)
    zip_code = models.TextField(null=True)
    default = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BuyerReward(models.Model):
    user = models.ForeignKey(BuyerInfo, on_delete=models.CASCADE, related_name='buyer_reward_board', null=True, blank=True)
    point = models.IntegerField(blank=True)
    rank = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.user)

class BuyerInvitationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(null=True, max_length=300)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class BuyerRechargeHistory(models.Model):
    mobile = models.CharField(max_length=40)
    country = models.CharField(max_length=400, null=True)
    operator = models.CharField(max_length=400, null=True)
    amount = models.CharField(max_length=400, null=True)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class CartShop(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shop = models.ForeignKey('seller.ShopInfo',related_name='cart_shop', on_delete=models.CASCADE)

class CartItem(models.Model):
    cart_shop = models.ForeignKey(CartShop, related_name='cart_item', on_delete=models.CASCADE)
    product = models.ForeignKey('seller.ShopProduct', related_name='cart_item', on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=400)
    color_name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=1,null=True, blank=True)

class BankRecipt(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bank_user')
    transection_id = models.CharField(max_length=20)
    bank_reciept = models.ImageField(upload_to='bank_reciept/')