from django.urls import path
from . import views


urlpatterns = [
    path("general-setting/", views.general_setting, name="general_setting"),
    path("pos-setting/", views.pos_setting, name="pos_setting"),
path("", views.setting_home, name="setting_home"),
path("master-setting/", views.master_setting, name="master_setting"),
path("user/", views.user_setting, name="user_setting"),
path("sticker/", views.sticker_setting, name="sticker_setting"),
    path('add-pos-template/', views.add_pos_template, name='add_pos_template'),

    path('edit-template/<int:pk>/', views.edit_template, name='edit_template'),
    path('delete-template/<int:pk>/', views.delete_template, name='delete_template'),
path("price-code/", views.price_code, name="price_code"),

    path('check-update/', views.check_update_page, name='check_update'),
    path('run-update/', views.run_update, name='run_update'),

    path('customer-settings/', views.customer_setting_page, name='customer_setting'),
    path('customer-settings/save/', views.customer_setting_save, name='customer_setting_save'),

]
