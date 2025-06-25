from django.urls import path
from . import views


urlpatterns=[
    path("",views.bank_account, name="bank_account"),
path("statement/<uuid:id>",views.bank_statement, name="bank_statement"),
path("statement/",views.bank_statement, name="bank_statement"),
path("upload/",views.upload_file, name="bank_upload"),
path("reset/<uuid:id>",views.bank_reset, name="bank_reset"),
path('update-description/', views.update_bank_description, name='update_bank_description'),

]