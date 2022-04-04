from django.db import models
from django.contrib.auth.models import User
import uuid
from buyer.models import BuyerInfo
from django.db.models import Sum,Avg

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "tunibibi_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class BusinessType(models.Model):
    type_name = models.CharField(max_length=200)
    type_image = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_name


class ShopInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_auth', null=True, blank=True)
    business_country = models.CharField(max_length=200, null=True, blank=True)
    business_name = models.CharField(max_length=200, null=True)
    business_slug = models.SlugField(max_length=200, null=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.PROTECT, related_name='business_type', null=True,
                                      blank=True)
    mobile_number = models.CharField(max_length=20)
    business_address = models.TextField(null=True)
    reg_ip = models.GenericIPAddressField(null=True)
    business_logo = models.ImageField(default='default/default-logo.png', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    followers = models.ManyToManyField(BuyerInfo, null=True)

    def __str__(self):
        return str(self.user)

class ShopOverView(models.Model):
    shop = models.ForeignKey(ShopInfo, on_delete=models.CASCADE, related_name='shop_overview')

    @property
    def followers_count(self):
        number_of_followers = self.shop.followers.count()
        return number_of_followers

    @property
    def positive_feedback(self):
        positive_feedback = Review.objects.filter(product__user=self.shop.user)
        total_ratings = positive_feedback.aggregate(Sum('ratings'))
        total_review = positive_feedback.count()
        calculate_avg = (total_ratings['ratings__sum'] * 100.0/ (total_review * 5.0))
        return calculate_avg

    @property
    def product_count(self):
        product_count = ShopProduct.objects.filter(user = self.shop.user).count()
        return product_count

class ShopOnlineStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_online', null=True, blank=True)
    online_status = models.BooleanField(default=True)
    scheduled_online_time = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HomePromoBanner(models.Model):
    banner = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class ProductSubcategory(models.Model):
    parent_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_category')
    category_name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class ProductWeightUnit(models.Model):
    unit_name = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unit_name


class ShopProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_product', null=True, blank=True)
    name = models.TextField()
    slug = models.SlugField(max_length=255, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='sell_prod_category')
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.PROTECT, related_name='sell_prod_subcategory')
    wholesale_price = models.JSONField()
    product_details = models.TextField(null=True)
    weight = models.CharField(max_length=20)
    weight_unit = models.ForeignKey(ProductWeightUnit, on_delete=models.PROTECT, related_name='sell_weight_unit')
    video_url = models.URLField()
    product_origin = models.CharField(max_length=200)
    model_no = models.TextField(null=True, blank=True)
    country_code = models.TextField(null=True, blank=True)
    product_status = models.BooleanField(default=False)
    total_sale = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Live(models.Model):
    user = models.ForeignKey(ShopInfo,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    viewers = models.IntegerField(default=0)
    products = models.ManyToManyField(ShopProduct,null=True)

class Review(models.Model):
    product = models.ForeignKey(ShopProduct,on_delete=models.CASCADE, related_name='review', null=True, blank=True)
    user = models.ForeignKey(BuyerInfo,on_delete=models.CASCADE, related_name='review_user', null=True, blank=True)
    ratings = models.IntegerField()
    description = models.TextField()


class ProductVariant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='variant_user', null=True, blank=True)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='product_variant', null=True)
    name = models.CharField(max_length=200)
    color = models.FileField(upload_to=generate_filename, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductSizeStock(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='size_stock_variant')
    size = models.CharField(max_length=200)
    stock = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_user', null=True, blank=True)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='product_image', null=True)
    product_image = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BuyTogether(models.Model):
    item_need = models.IntegerField()
    buy_together_price = models.FloatField()
    time_end = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user')
    order_id = models.CharField(max_length=200, null=True, blank=True)
    item_count = models.IntegerField(default=0)
    item_total = models.FloatField(default=0)
    delivery_fee = models.FloatField(default=0)
    coupon_code = models.CharField(max_length=200, null=True, blank=True)
    coupon_discount = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    payment_method = models.CharField(max_length=200)
    order_status = models.CharField(max_length=200, default="Pending")
    delivery_time = models.CharField(max_length=200, null=True, blank=True)
    shipping_status = models.CharField(max_length=200, null=True, blank=True)
    order_date = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_item')
    buy_together = models.ForeignKey(BuyTogether,on_delete=models.PROTECT, null=True, related_name='buy_together_item')
    product_id = models.IntegerField()
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    subtotal = models.FloatField(default=0)
    color = models.TextField(null=True)
    size = models.TextField(null=True)


class Coupon(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_coupon')
    coupon_code = models.CharField(max_length=200)
    usage_per_customer = models.IntegerField(default=1)
    discount_type = models.CharField(max_length=200)
    discount_value = models.FloatField()
    minimum_order_value = models.FloatField()
    max_discount_amount = models.FloatField(blank=True)
    show_to_customer = models.BooleanField(default=False, blank=True)
    coupon_status = models.BooleanField(default=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CourierMethod(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_courier')
    courier_name = models.CharField(max_length=200)
    charge_per_kg = models.FloatField()
    free_above_amount = models.FloatField(default=-1, blank=True)


class PaymentMethods(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_pay_method')
    method_name = models.CharField(max_length=200)
    method_details = models.TextField(null=True)

class PaymentTransection(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='transection_order')
    payment_method = models.ForeignKey(PaymentMethods,on_delete=models.CASCADE,related_name='transection_method')
    transection_id = models.CharField(max_length=200)



class ExtraCharge(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_ec')
    vat = models.FloatField(default=0)
    tax = models.FloatField(default=0)


class Reward(models.Model):
    user = models.ForeignKey(ShopInfo, on_delete=models.CASCADE, related_name='reward_board', null=True, blank=True)
    point = models.IntegerField(blank=True)
    rank = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.user)


class InvitationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(null=True, max_length=300)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Point(models.Model):
    country = models.CharField(max_length=400, null=True)
    point = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.country


# referal code per point equal 10 point seller and buyer

class RewardForPoint(models.Model):
    country = models.CharField(max_length=400,null=True)
    point = models.IntegerField()
    money = models.IntegerField()

    def __str__(self):
        return self.country


class Operator(models.Model):
    country = models.CharField(max_length=400, null=True)
    operator = models.CharField(max_length=400, null=True)


class RechargeHistory(models.Model):
    mobile = models.CharField(max_length=40)
    country = models.CharField(max_length=400, null=True)
    operator = models.CharField(max_length=400, null=True)
    amount = models.CharField(max_length=400, null=True)


class seller_text(models.Model):
    message_one = models.CharField(max_length=1000, null=True)
    message_two = models.CharField(max_length=1000, null=True)
    message_three = models.CharField(max_length=1000, null=True)


class Product_deal(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, null=True)
    min_quality = models.CharField(max_length=400, null=True)
    max_quality = models.CharField(max_length=500, null=True)
    bdt = models.CharField(max_length=400, null=True)
    select_time = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.prodcut)


class Invitation_seller_text(models.Model):
    heading = models.CharField(max_length=1000, null=True)
    decleartion = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.heading
