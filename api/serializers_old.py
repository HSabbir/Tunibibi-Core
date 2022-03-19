from system.models import *
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class SellerRegistrationSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, required=True)

    def get_password(self):
        return self.password

    class Meta:
        model = Seller
        fields = ('name', 'country', 'city', 'address', 'whatsapp', 'email', 'password', 'store_type', 'store_name',
                  'store_logo', 'profile_photo')


class SellerDataSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    country = serializers.SerializerMethodField('get_country')
    city = serializers.SerializerMethodField('get_city')

    def get_country(self, obj):
        return CountrySerializer(obj.country).data

    def get_city(self, obj):
        return CitySerializer(obj.city).data

    def get_store_logo_url(self, instance):
        request = self.context.get('request')
        store_logo_url = instance.store_logo.url
        return request.build_absolute_uri(store_logo_url)

    def get_profile_photo_url(self, instance):
        request = self.context.get('request')
        profile_photo_url = instance.profile_photo.url
        return request.build_absolute_uri(profile_photo_url)

    class Meta:
        model = Seller
        fields = ('id', 'name', 'store_name', 'store_type', 'country', 'city', 'address', 'whatsapp', 'email',
                  'store_logo', 'profile_photo')


class CountrySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'flag']


class CitySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class CategorySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    def get_image_url(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'order_sequence']


class SubCategorySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    def get_image_url(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class UserRegistrationSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, required=True)

    def get_password(self):
        return self.password

    class Meta:
        model = Users
        fields = ['name', 'country', 'city', 'address', 'mobile', 'email', 'password', 'entrepreneur', 'store_name',
                  'profile_photo']


class UserDataSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    country = serializers.SerializerMethodField('get_country')
    city = serializers.SerializerMethodField('get_city')

    def get_country(self, obj):
        return CountrySerializer(obj.country).data

    def get_city(self, obj):
        return CitySerializer(obj.city).data

    def get_profile_photo_url(self, instance):
        request = self.context.get('request')
        profile_photo_url = instance.profile_photo.url
        return request.build_absolute_uri(profile_photo_url)

    class Meta:
        model = Users
        fields = ['name', 'country', 'city', 'address', 'mobile', 'email', 'entrepreneur', 'store_name',
                  'profile_photo']


class LiveStreamCreateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = LiveStreaming
        fields = ['schedule_datetime', 'duration', 'category', 'title', 'banner_image']


class LiveStreamDataSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def get_banner_image_url(self, instance):
        request = self.context.get('request')
        banner_image_url = instance.banner_image.url
        return request.build_absolute_uri(banner_image_url)

    class Meta:
        model = LiveStreaming
        fields = ['id', 'category', 'title', 'banner_image', 'schedule_datetime', 'end_datetime', 'duration']


class LiveStreamStatReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    live = serializers.SerializerMethodField('get_live')

    def get_live(self, obj):
        return LiveStreamDataSerializer(obj.live).data

    class Meta:
        model = LiveStreamStatistics
        fields = ['live', 'views', 'reaction', 'comments']


class LiveStreamStatUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = LiveStreamStatistics
        fields = ['live', 'views', 'reaction', 'comments']
