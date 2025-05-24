from datetime import date

from django.forms import ModelForm, DateInput
from .models import *
from django import forms

class Staff_Form(ModelForm):

    class Meta:

        model = Staff
        fields='__all__'
        exclude = ('company','sync', 'discontinued', 'exit_date')

        widgets = {
            'join_date': DateInput(attrs={'type': 'date'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
