#!/usr/bin/env python
# -*- coding: utf-8 -*-

from erp.news_management.models import News
from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
#from django.db import connection
#connection.text_factory = lambda x: x.decode('cp1251').encode('utf-8')

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News

class EmployeeAdmin(admin.ModelAdmin):
    form = NewsAdminForm

admin.site.register(News, EmployeeAdmin)