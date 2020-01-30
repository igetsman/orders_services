#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from erp.comment_management.models import Comment

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea,label="Комментарий")
    class Meta:
        model = Comment
        fields = ['text']