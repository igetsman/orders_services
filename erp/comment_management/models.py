#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from erp.employee_management.models import CustomUser

class Comment(models.Model):
    author = models.ForeignKey(CustomUser)
    type = models.CharField(max_length=16)
    object_id = models.PositiveIntegerField()
    text = models.TextField(max_length=256)
    date = models.DateTimeField()

    def __unicode__(self):
        return str(self.text)

