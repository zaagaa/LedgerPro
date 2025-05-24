from django.forms import ModelForm
from . models import *


class Purchase_Form(ModelForm):
    class Meta:
        model=Purchase
        fields= '__all__'


class Stock_Form(ModelForm):
    class Meta:
        model=Stock
        fields= '__all__'


# from django import forms
#
# class MultiplePurchaseScanForm(forms.Form):
#     images = forms.FileField(
#         widget=forms.FileInput(attrs={'multiple': True, 'class': 'form-control'}),
#         required=False
#     )
