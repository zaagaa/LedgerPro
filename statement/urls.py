from django.urls import path
from . import views




urlpatterns = [
path('bill-wise/', views.bill_wise, name='statement_bill_wise'),
path('day-wise/', views.day_wise, name='statement_day_wise'),
path('sales-report/', views.report, name='statement_report'),
path('invoice/modal/<int:pk>/', views.invoice_modal_view, name="invoice_modal_view"),
path('gstr1/summary/', views.gstr1_summary, name='gstr1_summary'),
path("hsn-invoice-details/", views.hsn_invoice_details, name="hsn_invoice_details"),

path('invoice/month-wise-sales/', views.month_wise_sales_summary, name='month_wise_sales'),
path('sales/year-wise-summary/', views.year_wise_sales_summary, name='year_wise_sales'),
path('sales/inventory-summary/', views.inventory_wise_sales_summary, name='inventory_wise_sales'),
path('sales/inventory-analysis/', views.inventory_trend_analysis, name='inventory_trend_analysis'),


path('sales/floor_sale_report/', views.floor_sale_report, name='sales_breakdown_report'),
path('ajax/inventory-breakdown/', views.inventory_breakdown, name='inventory_breakdown'),

path('report/analysis/', views.analysis_report, name='analysis_report'),
path('cash_flow_summary/', views.cash_flow_summary, name='cash_flow_summary'),
path('daily-sales-chart/', views.daily_sales_chart, name='daily_sales_chart'),
]
