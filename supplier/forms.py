from django.forms import ModelForm

from purchase.models import Payment
from . models import *


# class Supplier_Form(ModelForm):
#     class Meta:
#         model=Supplier
#         fields= '__all__'

from django import forms


class PaymentForm(forms.ModelForm):
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    cheque_cleared = forms.BooleanField(required=False)
    cheque_given = forms.BooleanField(required=False)
    bank_checked = forms.BooleanField(required=False)

    class Meta:
        model = Payment
        fields = [
            'transaction_date',
            'description',
            'amount',
            'paid_by',
            'tran_no',
            'cheque_cleared',
            'cheque_given',
            'bank_checked',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Handle unbound and bound cases
        if instance:
            # Even if the form is bound, this forces initial values correctly
            self.initial['cheque_cleared'] = instance.cheque_cleared == 1
            self.initial['cheque_given'] = instance.cheque_given == 1
            self.initial['bank_checked'] = instance.bank_checked == 1

        for name, field in self.fields.items():
            css = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            field.widget.attrs['class'] = css

    def clean_cheque_cleared(self):
        return 1 if self.cleaned_data.get('cheque_cleared') else 0

    def clean_cheque_given(self):
        return 1 if self.cleaned_data.get('cheque_given') else 0

    def clean_bank_checked(self):
        return 1 if self.cleaned_data.get('bank_checked') else 0




from django_countries import countries


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'tax_number', 'address', 'city', 'state', 'country', 'pincode', 'mobile', 'code_name']
        widgets = {
            'country': forms.Select(choices=countries, attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        default_country = kwargs.pop('default_country', None)
        super().__init__(*args, **kwargs)

        if default_country and not self.instance.pk:
            self.fields['country'].initial = default_country

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'

# class SupplierForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         default_country = kwargs.pop('default_country', None)
#         super().__init__(*args, **kwargs)
#
#         if default_country and not self.instance.pk:
#             self.fields['country'].initial = default_country
#
#         self.fields['mobile'].required = True
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             if field.required:
#                 field.widget.attrs['required'] = 'required'
#
#     class Meta:
#         model = Supplier
#         fields = [
#             'supplier_name', 'tax_number', 'address', 'city',
#             'state', 'country', 'pincode', 'mobile', 'code_name'
#         ]
#         widgets = {
#             'country': forms.Select(choices=countries, attrs={'class': 'form-control'})
#         }
