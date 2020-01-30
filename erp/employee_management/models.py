#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from erp.user_management.models import CustomUser
from ckeditor.fields import RichTextField
from erp.common import common

class Employee(models.Model):
    full_name = models.CharField( max_length=128)
    location = models.CharField(max_length=128)
    specialisation = models.CharField(max_length=256,choices=common.SPECIALISATION_CHOICES)
    description = RichTextField()
    price_per_m2 = models.FloatField()
    currency = models.CharField(max_length=3,choices=common.CURRENCY_CHOICES)
    contact_phone = models.CharField(max_length=16)
    contact_email = models.CharField(max_length=128)
    rating = models.IntegerField()
    user_id = models.ForeignKey(CustomUser)

    
    def __unicode__(self):
        return self.full_name

    def get_cname(self):
        class_name = self.__class__.__name__.lower()
        return class_name