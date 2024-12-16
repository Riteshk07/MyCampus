from django.db import models
from datetime import datetime


# Create your models here.
class Analytics(models.Model):
    ip = models.CharField(max_length=200, null=True)
    user_id = models.IntegerField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(default=datetime.now())
