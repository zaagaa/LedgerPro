from django.forms import ModelForm
from . models import *

class Purchase_Form(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

    def save(self, commit=True):
        import time
        instance = super().save(commit=False)
        instance.sync_unix = int(time.time() * 1000)
        if commit:
            instance.save()
        return instance


class Stock_Form(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

    def save(self, commit=True):
        import time
        instance = super().save(commit=False)
        instance.sync_unix = int(time.time() * 1000)
        if commit:
            instance.save()
        return instance



# from django import forms
#
# class MultiplePurchaseScanForm(forms.Form):
#     images = forms.FileField(
#         widget=forms.FileInput(attrs={'multiple': True, 'class': 'form-control'}),
#         required=False
#     )
