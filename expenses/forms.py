from django import forms
from .models import Cash_Flow_Expenses

class CashFlowExpensesForm(forms.ModelForm):
    class Meta:
        model = Cash_Flow_Expenses
        fields = ['entry_date', 'amount', 'description']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
