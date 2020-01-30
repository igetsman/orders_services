from django import forms
from erp.photo_management.models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model=Photo
        fields = ['title','image']