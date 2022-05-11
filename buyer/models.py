from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
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
    quantity = models.IntegerField(default=1,null=True, blank=True)