
from django.db import models

class ZipCode(models.Model):
    zipcode = models.CharField(max_length=5)

    class Meta:
        db_table = 'zipcodes'

class Year(models.Model):
    year_built = models.CharField(max_length=4)

    class Meta:
        db_table = 'years'
