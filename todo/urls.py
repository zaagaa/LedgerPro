from django.urls import path
from . import views




urlpatterns = [
path('', views.todo, name='todo'),
path('update-task-field/', views.update_task_field, name='update_task_field'),



]
