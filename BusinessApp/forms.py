from django import forms

class DatabaseSetupForm(forms.Form):
    ENGINE_CHOICES = [
        ('sqlite3', 'SQLite'),
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
    ]
    engine = forms.ChoiceField(choices=ENGINE_CHOICES)
    name = forms.CharField(required=False)
    user = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    host = forms.CharField(required=False)
    port = forms.CharField(required=False)