from .viewsets.product_viewsets import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('products',ProductViewset)
router.register('popular_products',PopularProducts)
router.register('live',LiveViewsets)