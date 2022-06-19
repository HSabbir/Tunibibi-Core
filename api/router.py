from .viewsets.product_viewsets import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('products',ProductViewset)
router.register('get_orders',OrderViewset)
router.register('order_tracker',OrderTrackerView)
router.register('popular_products',PopularProducts)
router.register('live',LiveViewsets),
router.register('shop_overview',ShopOverView),
router.register('buytogether',BuyTogether),
router.register('buyer_save_folder',FolderViewset,basename='BuyerFolderToSaveProduct')

router.register('all_color',GetAllColor)
router.register('all_size',GetAllSize)
router.register('get_all_folder',GetAllFolderOfBuyer, basename='BuyerFolderToSaveProduct')
router.register('shipping_address',ShippingAddressViewsets)