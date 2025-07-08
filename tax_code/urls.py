from django.urls import path
from . import views


urlpatterns = [
path('', views.tax_code, name='tax_code'),
path('tax_code/delete/<uuid:id>', views.delete_tax_code, name='delete_tax_code'),
path('import/', views.import_data, name='import_tax_code'),
path('tax_code/save/', views.save_tax_code, name='save_tax_code'),
path('tax_code/delete-unused-ids/', views.delete_unused_ids, name='delete_unused_taxcode'),
]
