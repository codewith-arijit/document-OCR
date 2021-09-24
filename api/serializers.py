
from django.db.models import fields
from rest_framework import serializers
from .models import PanCard
from .models import AdharCard
from .models import VoterCard
from .models import DriverCard
from .models import Bank
from api import models

class PanCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PanCard
        fields = ('id','name', 'image')

        
class AdharCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdharCard
        fields = ('id','name', 'image')


class VoterCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VoterCard
        fields = ('id','name', 'image')


class DriverCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DriverCard
        fields = ('id','name', 'image')

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'file', 'choices')
