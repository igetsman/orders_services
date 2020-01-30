from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    user_id = models.OneToOneField(User, primary_key=True)
    custom_description = models.CharField(max_length=256)
    custom_phone = models.CharField(max_length=16)
    custom_email = models.CharField(max_length=128)




