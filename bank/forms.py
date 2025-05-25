from django.forms import ModelForm
from . models import *
from django import forms





class Bank_Account_Form(forms.ModelForm):
    class Meta:
        model=Bank_Account
        fields= '__all__'




