from django.urls import path
from . import views
from .views import Purchase_Stock_Table

urlpatterns = [
    path("", views.purchase_home, name="purchase"),
path("add_stock/<int:id>/", views.purchase_add_stock, name="purchase_add_stock"),
    path("query/<str:query>/", views.purchase_query, name="purchase_query"),
    # path("purchase_stock_table/", Purchase_Stock_Table.as_view(), name="purchase_stock_table"),

    path("purchase_stock_table/<int:id>/", views.purchase_stock_table_ajax, name="purchase_stock_table"),
path('save-columns/', views.save_column_preference, name='save_column_preference'),

path("purchase_stock_form/<int:id>/<int:edit_id>/", views.purchase_stock_form_ajax, name="purchase_stock_form"),
    path("delete_stock/<int:id>/", views.delete_stock, name="purchase_delete_stock"),
path("update/<int:id>/<str:field>/<str:value>/", views.purchase_field_update, name="purchase_field_update"),
path("sticker/", views.purchase_sticker, name="purchase_sticker"),
path('get-hidden-fields/', views.get_hidden_fields, name='get_hidden_fields'),
    path('save-hidden-fields/', views.save_hidden_fields, name='save_hidden_fields'),
path('purchase-statement/', views.purchase_statement, name='purchase_statement'),
path('purchase/<int:purchase_id>/upload-scan/', views.upload_purchase_scans, name='upload_purchase_scan'),
    path('serve-scan/<str:filename>/', views.serve_purchase_scan, name='serve_purchase_scan'),
path('purchase/scan/delete/<int:scan_id>/', views.delete_purchase_scan, name='delete_purchase_scan'),
path('purchase/<int:purchase_id>/finish-upload/', views.purchase_upload_finish, name='purchase_upload_finish'),

path('purchase/<int:purchase_id>/edit-company-supplier/', views.edit_purchase_company_supplier, name='edit_purchase_company_supplier'),
    path('ajax/get-suppliers/', views.get_suppliers_by_company, name='get_suppliers_by_company'),

path('stock/purchase/get-input-widths/', views.get_input_widths, name='get_input_widths'),
path('stock/purchase/save-input-widths/', views.save_input_widths, name='save_input_widths'),

path('update-supplier-margin/<int:supplier_id>/', views.update_supplier_margin, name='update_supplier_margin'),

    path('stock/expiry-list/', views.expiry_list_view, name='expiry_list'),

]
