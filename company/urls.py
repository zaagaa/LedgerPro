from django.urls import path
from . import views

urlpatterns = [
path('', views.company_index, name='company_index'),
# path('delete/<int:id>', views.delete_company, name='delete_company'),
    path('add/', views.company_form_view, name='company_add'),
    path('edit/<int:pk>/', views.company_form_view, name='company_edit'),
path('delete/<int:pk>/', views.company_delete, name='company_delete'),
path('get_states/', views.get_states, name='get_states'),

    path('company/add/', views.edit_or_add_company, name='company_add'),
    path('company/<int:pk>/edit/', views.edit_or_add_company, name='company_edit'),
path('ajax/get-states/', views.get_states_by_country, name='get_states_by_country'),

]
