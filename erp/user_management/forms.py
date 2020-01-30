#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from erp.user_management.models import CustomUser
from django.contrib.auth.models import User

class CustomUserForm(forms.ModelForm):
    custom_description = forms.CharField(label='Краткое описание')
    custom_phone = forms.CharField(label='Телефон')
    custom_email = forms.CharField(label='E-mail')
    class Meta:
        model=CustomUser
        fields = ['custom_description','custom_phone','custom_email']
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['first_name','last_name']