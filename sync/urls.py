from django.urls import path
from . import views
from .views import *



urlpatterns = [
path('api/', views.api, name='api'),
path('send/', views.master, name='sync_send'),
path('receive/', views.slave, name='sync_receive'),

]
