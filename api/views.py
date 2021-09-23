from django.db.models import query
from django.db.models.query import QuerySet
from django.http import request
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
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
from django.http import Http404
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
def PanCardView(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        pancard = PanCard.objects.all()
        serializer = PanCardSerializer(pancard, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PanCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['image']
            #print(image_path)
            result = ocr(settings.MEDIA_ROOT_URL + image_path)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)