#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from erp.user_management.models import CustomUser
from ckeditor.fields import RichTextField

class News(models.Model):
    description = RichTextField()
    date = models.DateTimeField()
    rating = models.IntegerField()
    user_id = models.ForeignKey(CustomUser)

    def __unicode__(self):
        return self.full_name

    def get_cname(self):
        class_name = self.__class__.__name__.lower()
        return class_name