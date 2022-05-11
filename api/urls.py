from django.urls import path, include

from .views import *
from .router import *

urlpatterns = [
    path('seller/check-existing-number', checkExistingMobileNumber),
    path('seller/set-password', setPassword),
    path('seller/change-password', changePassword),

    path('seller/token', tokenObtainPair),
    path('seller/token/refresh', tokenRefresh),
    path('seller/token/verify', tokenVerify),

    path('seller/business-types', getBusinessTypes),
    path('seller/create-shop', createShop),
    path('seller/update-shop-address', updateShopAddress),
    path('seller/shop-info', getShopInfo),
    path('seller/update-shop-info', updateShopInfo),

    path('seller/shop-online-status', getShopOnlineStatus),
    path('seller/go-online', goShopOnline),
    path('seller/go-offline', goShopOffline),

    path('seller/get-promo-banners', getPromoBanners),
    path('seller/get-home-overview', getHomeOverview),

    path('seller/product/get-weight-units', getWeightUnits),
    path('seller/product/get-category', getCategoryList),
    path('seller/product/get-subcategory', getSubcategoryList),
    path('seller/product/get-category-tree', getCategoryTree),

    path('seller/product/add-variant', addProductVariant),
    path('seller/product/edit-variant', editProductVariant),
    path('seller/product/delete-variant', deleteProductVariant),

    path('seller/product/add-product', addProduct),
    path('seller/product/add-product-image', addProductImage),
    path('seller/product/delete-product-image', deleteProductImage),

    path('seller/product/get-products', getShopProducts),
    path('seller/product/get-product-details', getShopProductDetails),

    path('seller/product/edit-product', editProduct),

    path('seller/product/update-product-status', updateProductStatus),
    path('seller/product/delete-product', deleteProduct),

    path('seller/order/get-orders', getOrders),
    path('seller/order/get-order-details', getOrderDetails),
    path('seller/order/accept-order', acceptOrder),
    path('seller/order/cancel-order', cancelOrder),
    path('seller/order/ship-order', shipOrder),
    path('seller/order/complete-order', completeOrder),
    path('seller/order/failed-order', failedOrder),

    path('seller/coupon/create-coupon', createCoupon),
    path('seller/coupon/get-coupons', getCoupons),

    path('seller/courier-method/create-courier', createCourier),
    path('seller/courier-method/get-courier', getCourier),

    path('seller/payment-method/get-methods', getPaymentMethod),
    path('seller/payment-method/update-methods', updatePaymentMethod),

    path('seller/my-payments', myPayments),
    path('seller/my-qr', myQR),

    path('seller/extra-charge/get-charge', getExtraCharge),
    path('seller/extra-charge/update-charge', updateExtraCharge),
    # Customer Side API
    path('customer/token', tokenObtainPair),
    path('customer/token', tokenObtainPair),

    path('customer/token/refresh', tokenRefresh),
    path('customer/token/verify', tokenVerify),

    path('customer/create', createCustomer),
    path('customer/place-order', placeOrder),

    # Reward/leaderboard
    path('customer/invite', invitation),
    path('leaderboard', getLeaderboard),
    path('rewardforpoint', RewardForPoint),
    path('getreward/<str:country>', getrewardbycountry),

    path('createoperator', createoperator),
    path('getoperators', getoperator),

    path('claimrecharge', claimrecharge),
    path('how_it_works',how_it_works),

    path('current_status',current_status),
    path('reward_post',reward_post),

    path('post_referal_point',post_referal_point),

    path('buyer/createaccount',createBuyerAccount),
    path('buyer/token',tokenObtainBuyer),
    path('buyer/invitation',buyerinvitation),

    path('createreview',createReview),
    path('getreview/<int:pk>',getReview),

    path('buyer/',include(router.urls)),

    path('buyer/getLeaderboard',getBuyerLeaderboard),
    path('buyer/get_current_rank',current_buyer_status),
    path('buyer/claimrecharge',buyerclaimrecharge),
    path('buyer/seller_recomended/<int:pk>',getSellerRecomendedProducts),
    path('buyer/all_item/<int:pk>',getSeller_all_item),

    path('buyer/follow',follow),
    path('buyer/place-order',placeOrder),

    path('buyer/updateProfile',updateProfile),
    path('buyer/add_product_existing_folder/<int:pk>',add_product_existing_folder),

    path('buyer/get_cart',get_cart),
    path('buyer/add_to_cart',add_to_cart),
    path('buyer/update_cart',update_cart),
    path('buyer/remove_cart_item',remove_cart_item),
    path('buyer/remove_cart_item_by_store',remove_cart_item_by_store),
    path('buyer/remove_all_item',remove_all_item)

]
