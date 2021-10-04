from django.conf import settings

import pytesseract
import cv2
import re

import cv2
import ftfy
from PIL import Image

#from scipy.ndimage import rotate
import numpy as np
face_classifier = cv2.CascadeClassifier("/home/arijitsen/Downloads/haarcascade_frontalface_default.xml")

def adhar(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    
    i = cv2.imread(filename)
    newdata=pytesseract.image_to_osd(i)
    angle = re.search('(?<=Rotate: )\d+', newdata).group(0)
    angle = int(angle)
    i = Image.open(filename)
    if angle != 0:
       #with Image.open("ro2.jpg") as i:
        rot_angle = 360 - angle
        i = i.rotate(rot_angle, expand="True")
        i.save(filename)
    
    i = cv2.imread(filename)
    # Convert to gray
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    i = cv2.dilate(i, kernel, iterations=1)
    i = cv2.erode(i, kernel, iterations=1)
    
    text = pytesseract.image_to_string(i)
    #return text
    # Arijit Code Added
    
    dict = text.split(' ')
    #print(dict)         

    #print('Pan card number is {}.\nDate of Birth is {}.'.format(val[0][0],val[1][0]))
    #print('\n')
    # Cleaning all the gibberish text
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    
    new_text = clear_text(text)
    #print(type(new_text))
    face_detect(filename)
    return new_text

def clear_text(text):
    list_text = []
    res = text.split()
    split_ocr = text.split('\n')
    yob_patn = '[0-9]{4}'
    dob_patn = '\d+[-/]\d+[-/]\d+'
    adhar_number_patn = '[0-9]{4}\s[0-9]{4}\s[0-9]{4}'
    adhar_name_patn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'    
        
        # adhar_name_pattrn = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    name = 'NULL'
    for ele in split_ocr:
        match = re.search(adhar_name_patn, ele)
        if match:
            name = match.group()
            print('name :', name)
            list_text.append(name)
    if name == 'NULL':
        if 'Government' in res:
            index = res.index('India')
            name = res[index + 3] + " " + res[index + 4]
        elif 'GOVERNMENT' in res:
            index = res.index('INDIA')
            name = res[index + 3] + " " + res[index + 4]
        else:
            name = split_ocr[1] + " " + split_ocr[2]
        print('name :', name)
        list_text.append(name)
    aadhar_number = ''
    for word in res:
        if 'yob' in word.lower():
            yob = re.findall('d+', word)
            if yob:
                print('Year of Birth: ' + yob[0])
                list_text.append(yob[0])
        if len(word) == 4 and word.isdigit():
            aadhar_number = aadhar_number + word + ' '
    if len(aadhar_number) >= 14:
        print("Aadhar number is : " + aadhar_number)
        list_text.append(aadhar_number)
    else:
        aadhar_number = 'NULL'
        print("Aadhar number not read")
    if aadhar_number == 'NULL':
        match = re.search(adhar_number_patn, text)
        print(match, 'match --3')
        if match:
            print(match.group(), 'match.group()')
            aadhar_number = match.group()
            print("Aadhar number is : " + aadhar_number)
            list_text.append(aadhar_number)
    if 'DOB' in text:
        match = re.search(dob_patn, text)
        if match:
            DateOfBirth = match.group()
            print('DateOfBirth :', DateOfBirth)
            list_text.append(DateOfBirth)
    elif 'DOB:' in res:
        match = re.search(dob_patn, text)
        if match:
            DateOfBirth = match.group()
            print('DateOfBirth :', DateOfBirth)
            list_text.append(DateOfBirth)
    else:
        match = re.search(dob_patn, text)
        if match:
            DateOfBirth = match.group()
            print('DateOfBirth :', DateOfBirth)
            list_text.append(DateOfBirth)
    if 'Year of Birth' in text:
        match = re.search(yob_patn, text)
        if match:
            DateOfBirth = match.group()
            print('DateOfBirth :', DateOfBirth)
            list_text.append(DateOfBirth)
    if 'Male' in text or 'MALE' in text:
        GENDER = 'Male'
    elif 'Female' in text or 'FEMALE' in text:
        GENDER = 'Female'
    else:
        GENDER = 'NAN'
    print('GENDER :', GENDER)
    list_text.append(GENDER)
    return list_text

    


def face_detect(filename):

    #print(filename, "XXX")
    img=cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('Original image', img)

    faces = face_classifier.detectMultiScale(gray, 1.3, 5)


    """if faces is ():
        print("No faces found")"""

    for (x, y, w, h) in faces:
        x = x - 25 
        y = y - 40 
        cv2.rectangle(img, (x, y), (x + w + 50, y + h + 70), (27, 200, 10), 2)
        #cv2.imshow('Face Detection', img)
        crop_img = img[y: y + h+70, x: x + w+50] 
        cv2.imwrite('/home/arijitsen/PAN-Card-OCR-master/media/Face1.jpg',crop_img)
        
        cv2.waitKey(1000)
    cv2.destroyAllWindows() 
    return crop_img