from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('category/', getCategoryList),
    path('country/', getCountryList),
    path('city/', getCityList),
    path('seller/registration/', sellerRegistration),
    path('user/registration/', userRegistration),
    path('livestream/create/', liveStreamCreate),
    path('livestream/all/', liveStreamAll),
    path('livestream/filter/', liveStreamFilter),
    path('livestream/statistics/', liveStreamStats),
    path('livestream/statistics/update/', liveStreamStatsUpdate),

]
