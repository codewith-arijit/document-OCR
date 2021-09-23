from django.db.models import query
from django.db.models.query import QuerySet
from django.http import request
from rest_framework.serializers import Serializer
from pcard.forms import ImageUploadForm
from django.conf import settings
from numpy import generic
from rest_framework import generics, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .models import PanCard
from .serializers import PanCardSerializer
from .ocr import ocr

class PanCardView(generics.ListCreateAPIView):
    queryset = PanCard.objects.all()
    serializer_class = PanCardSerializer
    
    ##############################################################################################
class PanCardViewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PanCard.objects.all()
    serializer_class = PanCardSerializer
    
