from django.contrib import admin

from .models import *


@admin.register(BuyerInfo)
class BuyerInfoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_number')

@admin.register(BuyerReward)
class RewardModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'rank')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartShop)
admin.site.register(BankRecipt)
admin.site.register(BuyerSgippingAddress)