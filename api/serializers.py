
from django.db.models import fields
from rest_framework import serializers
from .models import PanCard

class PanCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PanCard
        fields = ('id','name', 'image')

        
