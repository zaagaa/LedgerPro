from django.urls import path
from . import views




urlpatterns = [
path('', views.inventory, name='inventory'),
path('inventory/delete/<int:id>', views.delete_inventory, name='delete_inventory'),
path('inventory/delete-unused/', views.delete_unused_inventory, name='delete_unused_inventory'),

    path("manage/inventory/", views.manage_inventory, name="manage_inventory"),
    path("ajax/get-sections/", views.get_sections, name="get_sections"),
path('tax-slab/', views.tax_slab_list_create, name='tax_slab_list_create'),
path('tax-slab/edit/<int:slab_id>/', views.edit_tax_slab, name='edit_tax_slab'),
path('tax-slab/delete/<int:slab_id>/', views.delete_tax_slab, name='delete_tax_slab'),


]
