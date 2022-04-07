from django.contrib import admin

from .models import *


@admin.register(BuyerInfo)
class BuyerInfoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_number')

@admin.register(BuyerReward)
class RewardModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'rank')