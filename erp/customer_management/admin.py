#!/usr/bin/env python
# -*- coding: utf-8 -*-

from erp.customer_management.models import Customer
from django.contrib import admin
from django import forms


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer

class CustomerAdmin(admin.ModelAdmin):
     form = CustomerAdminForm


admin.site.register(Customer, CustomerAdmin)