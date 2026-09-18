from django.forms import ModelForm
from .models import *

class Customer_Form(ModelForm):

    class Meta:

        model = Customer
        fields='__all__'

