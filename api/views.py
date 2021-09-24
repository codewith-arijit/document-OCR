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

from .models import PanCard, AdharCard, VoterCard, DriverCard, Bank

from .serializers import PanCardSerializer, AdharCardSerializer, VoterCardSerializer, DriverCardSerializer,BankSerializer

from .ocr import ocr
from .adhar import adhar
from .voterid import voterid
from .driver import driver_license
from .bank import bank_details_alla, bank_details_sbi, bank_details_yes
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


@api_view(['GET', 'POST'])
def AdharCardView(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        adharcard = AdharCard.objects.all()
        serializer = AdharCardSerializer(adharcard, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdharCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['image']
            #print(image_path)
            result = adhar(settings.MEDIA_ROOT_URL + image_path)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def VoterCardView(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        votercard = VoterCard.objects.all()
        serializer = VoterCardSerializer(votercard, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VoterCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['image']
            #print(image_path)
            result = voterid(settings.MEDIA_ROOT_URL + image_path)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def DriverCardView(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        drivercard = DriverCard.objects.all()
        serializer = DriverCardSerializer(drivercard, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DriverCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['image']
            #print(image_path)
            result = driver_license(settings.MEDIA_ROOT_URL + image_path)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def BankView(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        bank = Bank.objects.all()
        serializer = BankSerializer(bank, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['file']
            #print(image_path)
            temp = request.POST['select_bank']
            if temp == "SBI":
                result = bank_details_sbi(settings.MEDIA_ROOT_URL + image_path)
            elif temp == "Alla":
                result = bank_details_alla(settings.MEDIA_ROOT_URL + image_path)
            elif temp == "Yes":
                result = bank_details_yes(settings.MEDIA_ROOT_URL + image_path)
            
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
