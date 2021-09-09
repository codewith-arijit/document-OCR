from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import numpy as np
import urllib
import json
import cv2
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .forms import UploadImageForm
from .forms import ImageUploadForm
from .forms import UploadFileForm
# import our OCR function
from .ocr import ocr
import re
from .adhar import adhar
from .voterid import voterid
from .bank import bank_details


def first_view(request):
    return render(request, 'pcard/first_view.html', {})

def index(request):
    return render(request, 'pcard/index.html' , {})

def aadhar(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
 
            imageURL = settings.MEDIA_URL + form.instance.image.name
            print(settings.MEDIA_URL, "cgfcgvhvhvh")
            adhar_text = adhar(settings.MEDIA_ROOT_URL + imageURL)
            print(adhar_text, "HHH")
            #obj={
            #    'form':form, 'post':post, 'adhar_text': adhar_text, 'img_src' : imageURL 
            #}
            #adhar_text=json.loads(json.dumps(adhar_text))
            ad_name = adhar_text[0]
            ad_dob = adhar_text[2]
            ad_gender = adhar_text[3]
            ad_num = adhar_text[1]
            obj = {
                "Name": ad_name,
                "DOB": ad_dob,
                "Gender": ad_gender,
                "Number": ad_num
            }
            return render(request, 'pcard/aadhar.html', {"adhar_text":obj, 'img_src' : imageURL})

    else:
        form = ImageUploadForm()
    return render(request, 'pcard/aadhar.html',{'form':form})


def voter_id(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
 
            imageURL = settings.MEDIA_URL + form.instance.image.name
            #print(settings.MEDIA_URL, "cgfcgvhvhvh")
            voterid_text = voterid(settings.MEDIA_ROOT_URL + imageURL)
            
            #obj={
            #    'form':form, 'post':post, 'adhar_text': adhar_text, 'img_src' : imageURL 
            #}
            #adhar_text=json.loads(json.dumps(adhar_text))
            
            return render(request, 'pcard/voterid.html', {"voterid_text":voterid_text, 'img_src' : imageURL})

    else:
        form = ImageUploadForm()
    return render(request, 'pcard/voterid.html',{'form':form})
    

def uimage(request):
  if request.method == 'POST':
      form = UploadImageForm(request.POST, request.FILES)
      if form.is_valid():
          myfile = request.FILES['image']
          fs = FileSystemStorage()
          filename = fs.save(myfile.name, myfile)
          uploaded_file_url = fs.url(filename)
      return render(request, 'pcard/uimage.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
  
  else:
      form = UploadImageForm()
      return render(request, 'pcard/uimage.html', {'form': form})

def ocr_core(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
 
            imageURL = settings.MEDIA_URL + form.instance.image.name
            print(imageURL)
            extracted_text = ocr(settings.MEDIA_ROOT_URL + imageURL)
            #print(extracted_text)
            return render(request, 'pcard/pcard.html', {'form':form, 'post':post, 'extracted_text': extracted_text, 'img_src' : imageURL})

    else:
        form = ImageUploadForm()
    return render(request, 'pcard/pcard.html',{'form':form})



def bank_id(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
 
            fileURL = settings.MEDIA_URL + form.instance.file.name
            print(fileURL)
            bank_text = bank_details(settings.MEDIA_ROOT_URL + fileURL)
            #print(extracted_text)
            print(bank_text, "HHH")
            """
            
            b_no = bank_text[0]
            b_name = bank_text[1]
            b_code = bank_text[2]
            b_op_bal = bank_text[3]
            b_cl_bal = bank_text[4]
            b_t_debit = bank_text[5]
            b_t_credit = bank_text[6]
            b_t_bal = bank_text[7]
            obj = {
                "Credit" : b_t_credit,
                "Balance": b_t_bal
            }
            """
            obj = [
                bank_text[0],
                bank_text[1],
                bank_text[2],
                bank_text[3],
                bank_text[4],
                bank_text[5],
                bank_text[6],
                bank_text[7],
            ]
            list_text_as_a_string = json.dumps(obj, indent=2)
            return render(request, 'pcard/bank.html', {'form':form, 'bank_text': list_text_as_a_string})
            #return render(request, 'pcard/bank.html', {'form':form, 'bank_text': bank_text})

    else:
        form = UploadFileForm()
    return render(request, 'pcard/bank.html',{'form':form})

