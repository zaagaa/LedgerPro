# forms.py
from django import forms

from pos.models import Print_Template


class PrintTemplateForm(forms.ModelForm):
    class Meta:
        model = Print_Template
        fields = ['template_name', 'template']
        widgets = {
            'template_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter template name'}),
            'template': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter template content', 'rows': 10}),
        }
