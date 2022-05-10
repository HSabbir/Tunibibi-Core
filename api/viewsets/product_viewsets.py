from ..importFile import *

from django_filters import rest_framework as filters_b
from .mixins import GetSerializerClassMixin
from ..decorators import  buyer_only
from rest_framework import viewsets
from rest_framework import filters

class ProductFilter(filters_b.FilterSet):
    user = filters_b.NumberFilter(field_name="user__id", lookup_expr="iexact")
    min_price = filters_b.NumberFilter(field_name="basic_price", lookup_expr='gte')
    max_price = filters_b.NumberFilter(field_name="basic_price", lookup_expr='lte')

    category = filters_b.CharFilter(field_name="category__category_name",lookup_expr='iexact')
    color = filters_b.CharFilter(field_name="product_variant__color",lookup_expr='iexact')
    size = filters_b.CharFilter(field_name="product_variant__size_stock_variant__size",lookup_expr='iexact')
    review = filters_b.NumberFilter(field_name="review__ratings",lookup_expr='iexact')
    origin = filters_b.CharFilter(field_name="product_origin",lookup_expr='iexact')
    class Meta:
        model = ShopProduct
        fields = ['user','category', 'color', 'size','review','min_price',
                  'max_price','origin']

class ProductViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductsReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,filters_b.DjangoFilterBackend]
    ordering_fields = ['created_at','basic_price','total_sale']
    search_fields = ['name', 'slug','category__category_name','subcategory__category_name','product_details','country_code']
    filter_class = ProductFilter


class PopularProducts(viewsets.ReadOnlyModelViewSet):
    queryset = ShopProduct.objects.filter(total_sale__gte = 5)
    serializer_class = ShopProductsReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class LiveViewsets(viewsets.ModelViewSet):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class ShopOverView(viewsets.ReadOnlyModelViewSet):
    queryset = ShopOverView.objects.all()
    serializer_class = ShopOverviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class BuyTogether(viewsets.ModelViewSet):
    queryset = BuyTogether.objects.all()
    serializer_class = BuyTogetherReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class GetAllFolderOfBuyer(viewsets.ReadOnlyModelViewSet):
    serializer_class = GetAllFolderName
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return BuyerFolderToSaveProduct.objects.filter(buyer=user)

class FolderViewset(GetSerializerClassMixin, viewsets.ModelViewSet):
    serializer_class = GetFolderWithProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters_b.DjangoFilterBackend]

    serializer_action_classes = {
        'create': AddFolderWithProductSerializer,
        'update':AddFolderWithProductSerializer
    }

    filterset_fields = ['folder_name']
    def get_queryset(self):
        user = self.request.user
        return BuyerFolderToSaveProduct.objects.filter(buyer=user)


class GetAllColor(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = GetColorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class GetAllSize(viewsets.ReadOnlyModelViewSet):
    queryset = ProductSizeStock.objects.all()
    serializer_class = GetSizeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

