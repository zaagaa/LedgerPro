from django.forms import ModelForm
from . models import *


class Invoice_Form(ModelForm):
    class Meta:
        model=Invoice
        fields= '__all__'