from os import name
from django.db import models
from numpy import mod

# Create your models here.

# Create your models here.
class PanCard(models.Model):
    
    name = models.CharField(max_length=255)
    image = models.ImageField()
    
class AdharCard(models.Model):
    
    name = models.CharField(max_length=255)
    image = models.ImageField()

class VoterCard(models.Model):
    
    name = models.CharField(max_length=255)
    image = models.ImageField()

class DriverCard(models.Model):
    
    name = models.CharField(max_length=255)
    image = models.ImageField()

class Bank(models.Model):
    
    file = models.FileField()
    
    
    choices = (
        ('SBI','State Bank Of India'),
        ('Alla','Allahabad Bank'),
        ('Yes','Yes Bank'),
    )  

    select_bank = models.CharField(max_length=4, choices=choices, default='green')