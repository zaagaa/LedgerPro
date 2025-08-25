# authentication/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'address', 'profile_image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
