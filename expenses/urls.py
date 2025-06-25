from django.urls import path
from . import views




urlpatterns = [
path('', views.expenses, name='expenses'),
path('cash-payment/', views.cash_payment, name='cash_payment'),
path('expenses-report/', views.expenses_report, name='expenses_report'),
path('add-expense/', views.add_cash_flow_expense, name='add_cash_flow_expense'),
path('delete-expense/', views.delete_cash_flow_expense, name='delete_cash_flow_expense'),
path('cash_flow_expense_list/', views.cash_flow_expense_list, name='cash_flow_expense_list'),

]
