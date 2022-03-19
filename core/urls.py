from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='core.home'),
    path('login/', login, name='core.login'),
    path('logout/', logout, name='core.logout'),

    path('system-settings/', systemSettings, name='core.system.settings'),
    path('edit-profile/', editProfile, name='core.edit.profile'),
    path('change-password/', changePassword, name='core.change.password'),
    path('change-user-password/', changeUserPassword, name='core.change.user.password'),

    path('administrators/', administrators, name='core.administrators'),
    path('administrators/ban/<int:user_id>/', administratorBan, name='core.administrators.ban'),
    path('administrators/unban/<int:user_id>/', administratorUnban, name='core.administrators.unban'),
    path('administrators/delete/<int:user_id>/', administratorDelete, name='core.administrators.delete'),

    path('legal/<str:doc_name>/', legal, name='core.legal'),

    path('country/', country, name='core.country'),
    path('country/toggle/<int:country_id>/', countryToggle, name='core.country.toggle'),
    path('country/delete/<int:country_id>/', countryDelete, name='core.country.delete'),

    path('city/', city, name='core.city'),
    path('city/status/', cityStatus, name='core.city.status'),
    path('city/delete/<int:city_id>/', cityDelete, name='core.city.delete'),

    path('category/', category, name='core.category'),
    path('category/edit/', categoryEdit, name='core.category.edit'),
    path('category/status/<int:category_id>/', categoryStatus, name='core.category.status'),
    path('category/sequence/', categorySequence, name='core.category.sequence'),
    path('category/delete/<int:category_id>/', categoryDelete, name='core.category.delete'),

    path('seller-list/', sellerList, name='core.seller.list'),
    path('seller-list/ban/<int:seller_id>/', sellerBan, name='core.seller.ban'),
    path('seller-list/unban/<int:seller_id>/', sellerUnban, name='core.seller.unban'),
    path('seller-list/delete/<int:seller_id>/', sellerDelete, name='core.seller.delete'),

    path('user-list/', userList, name='core.user.list'),
    path('user-list/ban/<int:user_id>/', userBan, name='core.user.ban'),
    path('user-list/unban/<int:user_id>/', userUnban, name='core.user.unban'),
    path('user-list/delete/<int:user_id>/', userDelete, name='core.user.delete'),

    path('live-schedule/', liveSchedule, name='core.live.schedule'),
    path('live-schedule/delete/<int:live_id>/', liveScheduleDelete, name='core.live.schedule.delete'),

    path('live-schedule/statistics/', liveScheduleStatistics, name='core.live.schedule.stats'),
]
