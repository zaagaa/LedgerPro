from django.urls import path
from . import views




urlpatterns = [
path('', views.supplier, name='supplier'),
path('supplier/delete/<uuid:id>', views.delete_supplier, name='delete_supplier'),
path('account/<str:id>', views.supplier_account, name='supplier_account'),
path('current_balance/', views.current_balance, name='supplier_current_balance'),
path('upcoming_payment/', views.upcoming_payment, name='supplier_upcoming_payment'),
path('payment/<uuid:pk>/edit/', views.edit_payment, name='edit_payment'),
path('payment/delete/<uuid:pk>/', views.delete_payment, name='delete_payment'),
path('invoice/pending/<uuid:id>/', views.invoice_pending, name='invoice_pending'),
    path('supplier/add/', views.edit_or_add_supplier, name='add_supplier'),
    path('supplier/<uuid:pk>/edit/', views.edit_or_add_supplier, name='edit_supplier'),
path('ajax/mark-cheque-given/', views.mark_cheque_given, name='mark_cheque_given'),
    path('sundry-creditors-chart/', views.sundry_creditors_chart, name='sundry_creditors_chart'),
path('ajax/payments-by-date/', views.payments_by_date, name='payments_by_date'),
]
