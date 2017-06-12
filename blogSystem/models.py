from __future__ import unicode_literals

from django.db import models

# Create your models here.

class test(models.Model):
    file_name = models.CharField(max_length=100)
    receivers = models.CharField(max_length=200)

    class Meta:
        db_table = 'test'