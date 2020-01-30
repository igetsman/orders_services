#!/usr/bin/env python
# -*- coding: utf-8 -*-

from erp.employee_management.models import Employee
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
#from django.db import connection
#connection.text_factory = lambda x: x.decode('cp1251').encode('utf-8')

# class EmployeeAdminForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         start_date = cleaned_data.get("start_date")
#         end_date = cleaned_data.get("end_date")
#         registration_deadline = cleaned_data.get('registration_deadline')
#         print start_date, end_date, registration_deadline
#         start_end_message = "Start Date must be before the End date of the Employee"
#         deadline_end_message = "Registration deadline must be before the end of the Employee"
#         if start_date >= end_date:
#             self._errors['start_date'] = ErrorList([start_end_message])
#             self._errors['end_date'] = ErrorList([start_end_message])
#
#             del cleaned_data['start_date']
#             del cleaned_data['end_date']
#         elif registration_deadline > end_date:
#             self._errors['registration_deadline'] = ErrorList([deadline_end_message])
#             self._errors['end_date'] = ErrorList([deadline_end_message])
#
#             del cleaned_data['registration_deadline']
#             del cleaned_data['end_date']
#         return cleaned_data
#
# class EmployeeAdmin(admin.ModelAdmin):
#     form = EmployeeAdminForm
#     fieldsets = [
#                  ('General Information', {'fields': ['full_name', 'description', 'location']}),
#                  ('Price Information', {'fields': ['price_per_m2', 'currency'], 'classes': ['collapse']})
#                  ]
#
# admin.site.register(Employee, EmployeeAdmin)