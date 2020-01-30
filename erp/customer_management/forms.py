#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from erp.customer_management.models import Customer
from ckeditor.widgets import CKEditorWidget
from erp.common import common

class CustomerForm(forms.ModelForm):
    full_name = forms.CharField(label="Полное имя")
    location = forms.CharField(label="Город")
    description = forms.CharField(widget=CKEditorWidget(),label="Описание заказа")
    currency = forms.ChoiceField(choices=common.CURRENCY_CHOICES,label="Валюта")
    typeofwork =  forms.ChoiceField(choices=common.TYPEOFWORK_CHOICES,label="Тип работ")
    price_per_m2 = forms.CharField(label="Предлагаемая цена")
    contact_phone = forms.CharField(label="Телефон")
    contact_email = forms.CharField(label="Электронная почта")
    modification_time = forms.HiddenInput()
    class Meta:
        model=Customer

