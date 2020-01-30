from django import forms
from erp.avator_management.models import Avator

class AvatorForm(forms.ModelForm):
    class Meta:
        model = Avator
        fields = ['image']