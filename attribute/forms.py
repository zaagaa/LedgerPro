from django.forms import ModelForm
from . models import *


class Attribute_Form(ModelForm):
    class Meta:
        model=Attribute
        fields= '__all__'



