from django.urls import path
from . import views


urlpatterns=[
    path("",views.attribute_index, name="attribute"),
path("data/<int:id>",views.attribute_data, name="attribute_data"),
path("delete_attribute/<int:id>",views.delete_attribute, name="delete_attribute"),
path("delete_attribute_data/<int:id>",views.delete_attribute_data, name="delete_attribute_data"),

]