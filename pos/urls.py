from django.urls import path
from . import views
from .views import *

urlpatterns = [
path('', views.pos, name='pos'),
path('query/', views.barcode_query, name='barcode_query'),
path('complete/',views.complete,name='pos_complete'),
path('bill_copy/',views.pos_bill_copy,name='pos_bill_copy'),
path('print_bill/',views.pos_print_bill,name='pos_print_bill'),
path('cancel_bill/',views.pos_cancel_bill,name='pos_cancel_bill'),
path('statement/',views.pos_statement,name='pos_statement'),

path('expenses/',views.pos_expenses,name='pos_expenses'),
path('ajax/autocomplete-description/', views.autocomplete_expense_description, name='autocomplete_expense_description'),

path('bill_list/',views.pos_bill_list,name='pos_bill_list'),
path('update/',views.pos_statement_update,name='pos_statement_update'),
path('bundle/',views.pos_bundle,name='pos_bundle'),
path('supplier_payment/',Pos_Supplier_payment.as_view(),name='pos_supplier_payment'),

path('add-staff-credit/', views.add_staff_credit, name='pos_add_staff_credit'),
path('ajax/staff-credit-info/', views.staff_credit_info_ajax, name='staff_credit_info_ajax'),

# path('pos/mark-session-printed/', views.mark_session_printed, name='mark_session_printed'),
# path('mark-as-printed/', views.mark_as_printed, name='mark_as_printed'),
# path('unprinted-logs/', views.unprinted_logs_view, name='unprinted_logs'),
# path('log-sale-entry/', views.log_sale_entry, name='log_sale_entry'),
# path("field-logs/", views.get_field_logs, name="get_field_logs"),  #  add this
# path("track-field-change/", views.track_field_change, name="track_field_change"),
# path('pos/visible-duration/', views.update_visible_duration, name='update_visible_duration'),

    path('staff-leave-booking/', views.staff_leave_booking, name='staff_leave_booking'),
    path('staff-leave-booking/delete/<uuid:id>/', views.delete_staff_leave, name='delete_staff_leave'),
    path('staff-leave-booking/add/', views.add_staff_leave, name='add_staff_leave'),

    path('proxy-print/<uuid:invoice_id>/', proxy_print_invoice, name='proxy_print_invoice'),


]
