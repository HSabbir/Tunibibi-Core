from django.contrib import admin
from .models import *


class BusinessTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name', 'type_image']


class HomePromoBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'banner']


class ProductWeightUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'unit_name']


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


admin.site.register(ShopOverView)
admin.site.register(BusinessType, BusinessTypesAdmin)
admin.site.register(HomePromoBanner, HomePromoBannerAdmin)
admin.site.register(ProductWeightUnit, ProductWeightUnitAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubcategory, ProductSubcategoryAdmin)


@admin.register(ShopProduct)
class ShopProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ShopInfo)
class ShopInfoModelAdmin(admin.ModelAdmin):
    list_display = ('id','mobile_number')

@admin.register(ProductVariant)
class ProductVariantModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name')


@admin.register(Reward)
class RewardModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'rank')


admin.site.register(InvitationCode)
admin.site.register(Point)


@admin.register(RewardForPoint)
class RewardForPointModelAdmin(admin.ModelAdmin):
    list_display = ('country', 'point', 'money')


@admin.register(Operator)
class OperatorModelAdmin(admin.ModelAdmin):
    list_display = ('country', 'operator')


@admin.register(RechargeHistory)
class OperatorModelAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'country', 'operator')


@admin.register(seller_text)
class seller_textModelAdmin(admin.ModelAdmin):
    list_display = ('message_one', 'message_two', 'message_three')


admin.site.register(Product_deal)

admin.site.register(ProductSizeStock)
admin.site.register(Review)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(BuyTogether )
admin.site.register(PaymentTransection)
admin.site.register(PaymentMethods)

admin.site.register(Coupon)
admin.site.register(BuyerFolderToSaveProduct)
admin.site.register(ProductImages)