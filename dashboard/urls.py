from django.urls import path
from . import views




urlpatterns = [
path('', views.dashboard_index, name='dashboard'),

path('select-company/<uuid:id>', views.dashboard_company, name='dashboard_company'),
path('update/', views.dashboard_update, name='update'),

path('notifications/clear/', views.clear_notifications, name='clear_notifications'),
path('notifications/', views.all_notifications, name='all_notifications'),


path('export/pdf/', views.dynamic_html_to_pdf, name='dynamic_html_to_pdf'),

]
