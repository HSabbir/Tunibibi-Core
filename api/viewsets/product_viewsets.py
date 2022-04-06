from ..importFile import *


from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework import filters

class ProductViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductsReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name', 'slug','category__category_name','subcategory__category_name','product_details','country_code']
    filterset_fields = ['category__category_name','subcategory__category_name','product_details','country_code']

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

class BuyTogether(viewsets.ReadOnlyModelViewSet):
    queryset = BuyTogether.objects.all()
    serializer_class = BuyTogetherReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
