from django.urls import path
from . import views

urlpatterns = [
path('', views.customer, name='customer'),
path('customer/save/', views.save_customer, name='save_customer'),
path('customer/get/', views.get_customer, name='get_customer'),
path('customer/delete/', views.delete_customer, name='delete_customer'),


path('points/', views.customer_point, name='customer_point'),
path('points/activities/', views.recent_activities, name='customer_activities'),
path('points/gift-otp/', views.gift_otp, name='customer_gift_otp'),
path('points/mobile_data/', views.mobile_data, name='mobile_data'),

# path('points/merge/', views.mobile_merge, name='mobile_merge'),

path("points/update-name/", views.update_customer_name, name="update_customer_name"),

path('points/transfer/', views.transfer_customer_points, name='transfer_points'),
path('points/customer-info/', views.get_customer_info, name='get_customer_info'),


path('points/reversal/', views.reverse_customer_point, name='customer_point_reversal'),
path('points/manual/', views.manual_point_entry, name='manual_point_entry'),
path('points/customer-lookup/', views.customer_lookup, name='customer_lookup'),


path('customer-point-info/', views.customer_point_info, name='customer_point_info'),



]
