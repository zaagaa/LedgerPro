from django.urls import path
from . import views




urlpatterns = [

    path('', views.staff_list, name='staff_list'),
path('staff/set-columns/', views.set_staff_columns, name='set_staff_columns'),


path('add/', views.add_staff, name='add_staff'),

    path('edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('discontinue/<int:staff_id>/', views.discontinue_staff, name='discontinue_staff'),
    path('rejoin/', views.rejoin_staff_page, name='rejoin_staff_page'),
    path('rejoin/confirm/<int:staff_id>/', views.rejoin_staff_confirm, name='rejoin_staff_confirm'),
    path('ajax/search-discontinued/', views.search_discontinued_staff, name='search_discontinued_staff'),
    path('staff/detail/ajax/', views.staff_detail_ajax, name='staff_detail_ajax'),
path('delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

path("early-comer-incentive/", views.early_comer_incentive, name="early_comer_incentive"),




# path('', views.staff, name='staff'),
# path('delete/<int:id>', views.delete_staff, name='delete_staff'),
# path('edit/<int:id>', views.edit_staff, name='edit_staff'),


path('attendance-entry/', views.attendance_entry, name='attendance_entry'),
# path('salary/<int:id>/', views.salary, name='salary'),
# path('salary/', views.salary, name='salary'),
    path("attendance-summary/", views.attendance_summary, name="attendance_summary"),
path('staff/credit/edit/', views.edit_staff_credit, name='edit_staff_credit'),
    path("add-credit/", views.add_staff_credit, name="add_staff_credit"),

path('payslip-quarter/', views.payslip_quartered, name='payslip_quartered'),

]
