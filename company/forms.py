from django import forms

from .models import Company

from django_countries import countries

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'tax_number', 'address', 'city', 'state', 'country', 'pincode', 'tax_type', 'mobile']
        widgets = {
            'country': forms.Select(choices=countries, attrs={'class': 'form-control'}),
            'tax_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'