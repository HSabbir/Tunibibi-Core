from django.contrib import admin

from .models import *

admin.site.register(BuyerInfo)

@admin.register(BuyerReward)
class RewardModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'rank')