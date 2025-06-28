from django.forms import ModelForm
from . models import *
from django import forms





class Tax_Code_Form(forms.ModelForm):
    class Meta:
        model=Tax_Code
        fields= '__all__'
        widgets={

            'tax_code': forms.NumberInput(attrs={'class':'form-control'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control'}),

        }



