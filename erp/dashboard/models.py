from django.db import models
from django.db import connection
connection.text_factory = lambda x: x.decode('cp1251').encode('utf-8')

# Create your models here.
