#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from erp.employee_management.models import Employee
from ckeditor.widgets import CKEditorWidget
from erp.common import common

class EmployeeForm(forms.ModelForm):
    full_name = forms.CharField(label="Полное имя")
    location = forms.CharField(label="Город")
    description = forms.CharField(widget=CKEditorWidget(),label="Описание услуг")
    specialisation = forms.ChoiceField(choices=common.SPECIALISATION_CHOICES,label="Специализация")
    currency = forms.ChoiceField(choices=common.CURRENCY_CHOICES,label="Валюта")
    price_per_m2 = forms.CharField(label="Цена")
    contact_phone = forms.CharField(label="Телефон")
    contact_email = forms.CharField(label="Электронная почта")
    class Meta:
        model=Employee