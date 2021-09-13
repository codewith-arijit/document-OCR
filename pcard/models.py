from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FileUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    choices = (
        ('SBI','State Bank Of India'),
        ('Alla','Allahabad Bank'),
        ('Yes','Yes Bank'),
    )  

    select_bank = models.CharField(max_length=4, choices=choices, default='green')
