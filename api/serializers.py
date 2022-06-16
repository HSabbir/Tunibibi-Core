from rest_framework.fields import DictField, CharField

from buyer.models import BuyerReward, BuyerRechargeHistory, Cart, CartItem, CartShop, BankRecipt, BuyerSgippingAddress
from seller.models import *
from customer.models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class EditBuyerSecurity(serializers.Serializer):
    current_password = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)
    new_re_password = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)

class ShopInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ['mobile_number']


class ShopInfoUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ['business_logo', 'business_name', 'business_type', 'business_address']


class PasswordInputValidator(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, required=True)
    password2 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ShopInfo
        fields = ['business_country', 'mobile_number', 'password1', 'password2']

class BuyerAccountValidator(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ShopInfo
        fields = ['business_country', 'mobile_number', 'password1']


class LoginSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ShopInfo
        fields = ['mobile_number', 'password']


class BusinessTypeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ['id', 'type_name', 'type_image']


class ShopCreateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ['business_name', 'business_type']


class ShopAddressUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ['business_address']


class ShopInfoReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    business_type = serializers.SerializerMethodField('get_business_type')
    business_type_id = serializers.SerializerMethodField('get_business_type_id')
    business_url = serializers.SerializerMethodField('get_business_url')
    email = serializers.SerializerMethodField('get_email')

    def get_email(self, instance):
        return instance.user.email

    def get_business_type(self, instance):
        try:
            return instance.business_type.type_name
        except Exception as e:
            return "Update Business Type"

    def get_business_type_id(self, instance):
        try:
            return instance.business_type.id
        except Exception as e:
            return "Update Business Type"

    def get_business_url(self, instance):
        return "tunibibi.com/s/%s" % instance.business_slug

    class Meta:
        model = ShopInfo
        fields = ['business_name', 'business_slug', 'business_url', 'business_type', 'business_type_id',
                  'mobile_number', 'business_address', 'business_logo', 'email']


class ShopOnlineStatusSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopOnlineStatus
        fields = ['online_status', 'scheduled_online_time']


class ShopOfflineUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopOnlineStatus
        fields = ['scheduled_online_time']


class HomeBannerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = HomePromoBanner
        fields = ['banner']


class HomeOverviewFilterSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)

    class Meta:
        model = ShopInfo
        fields = ['from_date', 'to_date']


class WeightUnitSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductWeightUnit
        fields = ['id', 'unit_name']


class ProductCategorySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'category_image']


class ProductCategoryTreeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField('get_subcategory')

    def get_subcategory(self, instance):
        sub_list = instance.product_category.all()
        return ProductSubcategorySerializer(sub_list, many=True, context={'request': self.context.get('request')}).data

    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'subcategory']


class ProductSubcategorySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = ['id', 'category_name', 'category_image']


class ProductAddVariantSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    size_stock = serializers.JSONField(required=True)

    class Meta:
        model = ProductVariant
        fields = ['name', 'color', 'size_stock']


class ProductEditVariantSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    variant_id = serializers.IntegerField(required=True)
    size_stock = serializers.JSONField(required=True)
    color = serializers.FileField(required=False)

    class Meta:
        model = ProductVariant
        fields = ['color', 'variant_id', 'name', 'size_stock']


class ProductAddVariantSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['name', 'color', 'user']


class ProductEditVariantSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    color = serializers.FileField(required=False)

    class Meta:
        model = ProductVariant
        fields = ['name', 'color']


class SizeStockSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductSizeStock
        fields = ['size', 'stock']


class ProductVariantReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    size_stock = serializers.SerializerMethodField('get_size_stock')

    def get_size_stock(self, instance):
        size_stocks = instance.size_stock_variant.all()
        return SizeStockSerializer(size_stocks, many=True).data

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'color', 'size_stock']


class AddProductSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    variant_id = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = ShopProduct
        fields = ['name', 'category', 'subcategory', 'wholesale_price', 'product_details', 'weight', 'weight_unit',
                  'video_url', 'product_origin', 'variant_id', 'model_no', 'country_code']


class AddProductSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['name', 'category', 'subcategory', 'wholesale_price', 'product_details', 'weight', 'weight_unit',
                  'video_url', 'product_origin', 'user', 'model_no', 'country_code']


class AddProductImageSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    product = serializers.IntegerField(required=True)
    images = serializers.JSONField(required=True)

    class Meta:
        model = ProductImages
        fields = ['product', 'images']


class AddProductImageSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['user', 'product', 'product_image']


class ProductImagesReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'product_image']


class DeleteProductImageSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    image_id = serializers.IntegerField(required=True)

    class Meta:
        model = ProductImages
        fields = ['image_id']


class ShopProductsReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    get_coupon = DictField(child=CharField())
    category = serializers.SerializerMethodField('get_category')
    subcategory = serializers.SerializerMethodField('get_subcategory')
    weight_unit = serializers.SerializerMethodField('get_weight_unit')
    weight_unit_id = serializers.SerializerMethodField('get_weight_unit_id')
    product_image = serializers.SerializerMethodField('get_product_image')
    variant = serializers.SerializerMethodField('get_variant')
    seller_id = serializers.SerializerMethodField('get_seller_id')
    shop_id = serializers.SerializerMethodField('get_shop')

    def get_seller_id(self,obj):
        return obj.user.id

    def get_shop(self,obj):
        return obj.user.seller_auth.id

    added_fav = serializers.SerializerMethodField('get_fav')

    def get_coupon(self,obj):
        try:
            coupon = Coupon.objects.filter(seller=obj.user)
            coupon = CouponSerializer(coupon,many=True)
            return coupon
        except:
            return None

    def get_seller(self,obj):
        shop = ShopInfo.objects.filter(user=obj.user)
        context = {
            "name": shop.business_name,
            "photo": shop.business_logo
        }
        return context

    def get_category(self, instance):
        return ProductCategorySerializer(instance.category, context={'request': self.context.get('request')}).data

    def get_subcategory(self, instance):
        return ProductSubcategorySerializer(instance.subcategory, context={'request': self.context.get('request')}).data

    def get_weight_unit(self, instance):
        return instance.weight_unit.unit_name

    def get_weight_unit_id(self, instance):
        return instance.weight_unit.id

    def get_product_image(self, instance):
        images = instance.product_image.all()
        return ProductImagesReadSerializer(images, many=True, context={'request': self.context.get('request')}).data

    def get_variant(self, instance):
        variants = instance.product_variant.all()
        return ProductVariantReadSerializer(variants, many=True, context={'request': self.context.get('request')}).data

    def get_fav(self,obj):
        product = BuyerFolderToSaveProduct.objects.filter(buyer=self.context.get('request').user, products__id=obj.id).exists()
        return product

    class Meta:
        model = ShopProduct
        fields = ['id', 'seller_id','seller_name','seller_photo','shop_id', 'name', 'slug', 'category', 'subcategory', 'wholesale_price', 'product_details', 'weight',
                  'weight_unit', 'weight_unit_id', 'video_url', 'product_origin', 'product_image', 'variant',
                  'product_status', 'model_no', 'country_code','basic_price','ratings','order_count',
                  'recent_buyer_name','recent_buyer_img','recent_buyer_qty','added_fav','get_coupon']


class ShopOverviewSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_user_name')
    img = serializers.SerializerMethodField('get_image')
    followers_count = serializers.ReadOnlyField()
    product_count = serializers.ReadOnlyField()
    positive_feedback = serializers.ReadOnlyField()
    class Meta:
        model = ShopOverView
        fields = ['shop','followers_count','product_count', 'positive_feedback','name','img']

    def get_user_name(self, Reward):
        try:
            name = ShopOverView.shop.business_name
            return name
        except:
            return ""

    def get_image(self, Reward):
        try:
            image = ShopOverView.shop.business_logo.url
            return image
        except:
            return ""

class FollowerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ['id','followers']

class LiveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = '__all__'

class ReviewSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    img = serializers.SerializerMethodField('get_image')


    class Meta:
        model = Review
        fields = ['product','user','ratings','description','img','name']
        read_only_fields = ('img','name')

    def get_name(self,obj):
        try:
            buyer = BuyerInfo.objects.filter(user=obj.user).first()
            return buyer.name
        except:
            return ""

    def get_image(self,obj):
        try:
            buyer = BuyerInfo.objects.filter(user=obj.user).first()
            return buyer.photo.url
        except:
            return ""


class ProductStatusUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)
    product_status = serializers.BooleanField(required=True)

    class Meta:
        model = ShopProduct
        fields = ['product_id', 'product_status']


class ProductStatusUpdateSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['product_status']


class ProductDeleteSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = ShopProduct
        fields = ['product_id']


class EditProductSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = ShopProduct
        fields = ['product_id', 'name', 'category', 'subcategory', 'wholesale_price', 'product_details', 'weight',
                  'weight_unit', 'video_url', 'product_origin', 'variant_id', 'model_no', 'country_code']


class EditProductSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['name', 'category', 'subcategory', 'wholesale_price', 'product_details', 'weight', 'weight_unit',
                  'video_url', 'product_origin', 'model_no', 'country_code']


class CreateCustomerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, required=True)
    password1 = serializers.CharField(max_length=200, required=True)
    password2 = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = CustomerInfo
        fields = ['name', 'mobile_number', 'country', 'address', 'city', 'postcode', 'password1', 'password2']


class CustomerInfoSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['user', 'name', 'country', 'address', 'city', 'postcode', 'point', 'rank']


class PlaceOrderSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    products = serializers.JSONField(required=True)
    token_discount = serializers.FloatField(required=False)

    class Meta:
        model = Orders
        fields = ['products', 'delivery_fee', 'coupon_code', 'coupon_discount', 'token_discount', 'payment_method']


class OrderItemSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product_id', 'quantity', 'unit_price', 'color', 'size']


class OrderItemSaveSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, instance):
        return instance.order_item.all().last().color

    class Meta:
        model = Orders
        fields = ['order_id', 'item_count', 'grand_total', 'payment_method', 'order_status', 'image', 'created_at']


class AllOrderInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class AllOrderProductSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class DetailsCustomerInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['name', 'mobile_number', 'country', 'address', 'city', 'postcode']


class AcceptOrderSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    order_id = serializers.CharField(max_length=200, required=True)
    delivery_time = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = Orders
        fields = ['order_id', 'delivery_time']


class OrderIDSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    order_id = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = Orders
        fields = ['order_id']


class CouponSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'usage_per_customer', 'discount_type', 'discount_value', 'minimum_order_value',
                  'max_discount_amount', 'show_to_customer', 'coupon_status']


class CourierMethodSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = CourierMethod
        fields = '__all__'


class CourierMethodReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = CourierMethod
        fields = ['id', 'courier_name', 'charge_per_kg', 'free_above_amount']


class PaymentMethodReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = ['id', 'method_name', 'method_details']


class PaymentMethodUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = ['id', 'method_details']


class ExtraChargeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ExtraCharge
        fields = ['vat', 'tax']


class LeaderBoardSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_mobile')
    name = serializers.SerializerMethodField('get_user_name')
    img = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Reward
        fields = ['user', 'point', 'rank', 'name', 'img']

    def get_mobile(self, Reward):
        user = Reward.user.mobile_number
        return user

    def get_user_name(self, Reward):
        name = Reward.user.business_name
        return name

    def get_image(self, Reward):
        image = Reward.user.business_logo.url
        return image

class BuyerLeaderBoardSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_mobile')
    name = serializers.SerializerMethodField('get_user_name')
    photo = serializers.SerializerMethodField('get_image')

    class Meta:
        model = BuyerReward
        fields = ['user', 'point', 'rank', 'name', 'photo']

    def get_mobile(self, BuyerReward):
        user = BuyerReward.user.mobile_number
        return user

    def get_user_name(self, BuyerReward):
        name = BuyerReward.user.name
        return name

    def get_image(self, BuyerReward):
        image = BuyerReward.user.photo.url
        return image


class RewardForPointSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = RewardForPoint
        # fields = '__all__'
        fields = ['country', 'point', 'money']


class OperatorSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class ClaimRechargeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = RechargeHistory
        fields = '__all__'

class BuyerClaimRechargeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = BuyerRechargeHistory
        fields = '__all__'


class Seller_textSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = seller_text
        fields = '__all__'


class PointSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'



class BuyTogetherReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField('get_buytogether')

    def get_buytogether(self,obj):
        order_item = OrderItems.objects.filter(buy_together=obj).first()
        return OrderItemSerializer(order_item, context={'request': self.context.get('request')}).data

    class Meta:
        model = BuyTogether
        fields = '__all__'


class BuyerInfoUpdateSerialiser(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    class Meta:
        model = BuyerInfo
        fields = ['name','country','mobile_number','address','photo','city','postcode']

        extra_kwargs = {
            "name": {"required": False},
            "country": {"required": False},
            "mobile_number" : {"required": False},
            "address" : {"required": False},
            "photo": {"required": False},
            "city": {"required": False},
            "postcode": {"required": False}
        }

class GetColorSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['name']

class GetSizeSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    class Meta:
        model = ProductSizeStock
        fields = ['size']


class AddFolderWithProductSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    class Meta:
        model = BuyerFolderToSaveProduct
        fields = ['folder_name','buyer','products']

class GetFolderWithProductSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    products = ShopProductsReadSerializer(many=True)
    class Meta:
        model = BuyerFolderToSaveProduct
        fields = ['folder_name','products']

class GetAllFolderName(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    class Meta:
        model = BuyerFolderToSaveProduct
        fields = ['id','folder_name']

class CartItems(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField('get_photo')
    product_price = serializers.SerializerMethodField('get_price')
    product_name = serializers.SerializerMethodField('get_name')

    def get_name(self,obj):
        return obj.product.name

    def get_price(self,obj):
        return obj.product.basic_price

    def get_photo(self,obj):
        try:
            images = ProductImages.objects.filter(product=obj.product).first()
            return images.product_image.url
        except:
            return ""

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','product_name','product_price', 'color','color_name','size','product_image']

class GetCartItem(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    cart_item = CartItems(many=True)
    shop_name = serializers.SerializerMethodField('get_name')
    shop_photo = serializers.SerializerMethodField('get_logo')

    def get_name(self,obj):
        return obj.shop.business_name

    def get_logo(self,obj):
        return obj.shop.business_logo.url

    class Meta:
        model = CartShop
        fields = ['cart_item','shop_name','shop_photo']


class UploadBankReciept(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    bank_reciept = serializers.ImageField(
        max_length=None)
    class Meta:
        model = BankRecipt
        fields = '__all__'

class BuyerShippingAddress(FriendlyErrorMessagesMixin,serializers.ModelSerializer):

    class Meta:
        model = BuyerSgippingAddress
        fields = ['id','buyer','name','country','mobile_number','street_address','apt_suite_unit','city',
                  'zip_code','default']
        read_only_fields = ['id']

class BuyerShippingAddressUpdate(FriendlyErrorMessagesMixin,serializers.ModelSerializer):

    class Meta:
        model = BuyerSgippingAddress
        fields = ['name','country','mobile_number','street_address','apt_suite_unit','city',
                  'zip_code','default']