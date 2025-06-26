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

    path('edit-template/<uuid:pk>/', views.edit_template, name='edit_template'),
    path('delete-template/<uuid:pk>/', views.delete_template, name='delete_template'),
path("price-code/", views.price_code, name="price_code"),

    path('check-update/', views.check_update_page, name='check_update'),
    path('run-update/', views.run_update, name='run_update'),

path('customer-settings/', views.customer_setting, name='customer_setting'),
    # path('customer-settings/', views.customer_setting_page, name='customer_setting'),
    # path('customer-settings/save/', views.customer_setting_save, name='customer_setting_save'),

    path('backup/', views.backup_restore_page, name="backup_restore_page"),
    path('backup/take/', views.take_backup, name="take_backup"),
    path('backup/restore/', views.restore_backup, name="restore_backup"),
    path('backup/download/<str:filename>/', views.download_backup, name="download_backup"),

path("staff-setting/", views.staff_setting, name="staff_setting"),

path("db-table-sizes/", views.database_tables_size, name="database_tables_size"),


]
