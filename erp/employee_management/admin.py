#!/usr/bin/env python
# -*- coding: utf-8 -*-

from erp.employee_management.models import Employee
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
#from django.db import connection
#connection.text_factory = lambda x: x.decode('cp1251').encode('utf-8')

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

admin.site.register(Employee, EmployeeAdmin)