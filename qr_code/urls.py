from django.urls import path
from .views import generate_qr_code

urlpatterns = [
    path('qr/<str:data>/', generate_qr_code, name='qr_code'),
]