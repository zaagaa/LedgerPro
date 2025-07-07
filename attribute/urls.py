from django.urls import path
from . import views


urlpatterns=[
    path("",views.attribute_index, name="attribute"),
path("data/<uuid:id>",views.attribute_data, name="attribute_data"),
path("delete_attribute/<uuid:id>",views.delete_attribute, name="delete_attribute"),
path("delete_attribute_data/<uuid:id>",views.delete_attribute_data, name="delete_attribute_data"),

]