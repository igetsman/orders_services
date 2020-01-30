#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from erp.news_management.models import News
from ckeditor.widgets import CKEditorWidget

class NewsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(),label="Текст новости")
    class Meta:
        model=News