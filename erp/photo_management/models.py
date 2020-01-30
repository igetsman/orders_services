#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from erp.employee_management.models import Employee

def content_file_name(instance, filename):
    return '/'.join([str(instance.employee.id),filename])

class Photo(models.Model):
    employee = models.ForeignKey(Employee)
    title = models.TextField(max_length=128)
    image = models.ImageField(upload_to=content_file_name)

    def __unicode__(self):
        return self.title

