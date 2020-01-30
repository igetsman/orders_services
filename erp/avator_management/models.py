#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from erp.employee_management.models import CustomUser

def content_file_name(instance, filename):
    return 'avators/'+str(instance.custom_user.user_id_id) +'/' + filename

class Avator(models.Model):
    custom_user = models.ForeignKey(CustomUser)
    image = models.ImageField(upload_to=content_file_name)

    def __unicode__(self):
        return str(self.image)

