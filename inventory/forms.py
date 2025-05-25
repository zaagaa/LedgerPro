from django.forms import ModelForm
from . models import *


class Inventory_Form(ModelForm):
    class Meta:
        model=Inventory
        fields= '__all__'




from django import forms
from .models import TaxSlab
from inventory.models import Inventory

class TaxSlabForm(forms.ModelForm):
    inventories = forms.ModelMultipleChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2'})
    )

    class Meta:
        model = TaxSlab
        fields = ['name', 'tax_rate', 'trigger_amount', 'inventories']