from os import name
from django.db import models
from numpy import mod

# Create your models here.

# Create your models here.
class PanCard(models.Model):
    
    name = models.CharField(max_length=255)
    image = models.ImageField()
    
