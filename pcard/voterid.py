from django.conf import settings

try:  
    from PIL import Image
except ImportError:  
    import Image
import pytesseract
import numpy as np
import cv2
import ftfy
import re
import json
import io
import os

face_classifier = cv2.CascadeClassifier("/home/arijitsen/Downloads/haarcascade_frontalface_default.xml")
                                        
#filename = cv2.imread("/home/arijitsen/PAN-Card-OCR-master/media")

def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def voterid(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    
    i = cv2.imread(filename)
    
    # Convert to gray
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    i = cv2.adaptiveThreshold(i, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((5,5), np.uint8)
    i = cv2.dilate(i, kernel, iterations=1)
    i = cv2.erode(i, kernel, iterations=1)
    
    text = pytesseract.image_to_string(i)
    #return text
    # Arijit Code Added
    dict = text.split(' ')
            
    
    print(dict, "XXX") 
    #print('Pan card number is {}.\nDate of Birth is {}.'.format(val[0][0],val[1][0]))
    print('\n')
    # Cleaning all the gibberish text
    #text = ftfy.fix_text(text)
    #text = ftfy.fix_encoding(text)
    #new_text = ocr_to_json(text)
    #face_detect(filename)
    #print(type(new_text))
    #list_text = new_text.split("\n")
    #print(list_text)

    new_text = get_name(text)
    face_detect(filename)
    file = open("../TextExtract.txt","w") 
    file.write(text)
    file.close()

    # new_text = text_process()
    return new_text



def get_name(text):
    # Initializing data variable
    name = None
    fname = None
    nameline = []
    text0 = []
    text1 = []
    text2 = []

    # Searching
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    # print(text1)
    text1 = list(
        filter(None, text1))  # Attribute has to be converted into a list object before any additional processing
    # print(text1) #at this operation the new line strings become a list of strings

    lineno = 0  # to start from the first line of the text file.

    for wordline in text1:
        xx = wordline.split('\n')
        if ([w for w in xx if re.search(
                '(ELECTOR|PHOTO|IDENTITY|CARD|ELECTION|COMMISSION|INDIA|IND|NDIA)$',
                w)]):
            text1 = list(text1)
            lineno = text1.index(wordline)
            break
    # text1 = list(text1)
    text0 = text1[lineno + 1:]
    # print(text0) #Contains all the relevant extracted text in form of a list - uncomment to check
    try:
        for x in text0:
            for y in x.split():
                # print(x)
                nameline.append(x)
                break
    except:
        pass
    # print(nameline)
    try:
        name = nameline[2].rsplit(':', 1)[1]
        fname = nameline[4].rsplit(':', 1)[1]

    except:
        pass
    # Making tuples of data
    data = {}
    data['Name'] = name
    data['Father Name'] = fname
    ##
    def findword(textlist, wordstring):
        lineno = -1
        for wordline in textlist:
            xx = wordline.split()
            if ([w for w in xx if re.search(wordstring, w)]):
                lineno = textlist.index(wordline)
                textlist = textlist[lineno+1:]
                return textlist
        return textlist

    # Finding the electors number 
    voter_no = findword(text1, '(ELECTION COMMISSION OF INDIA | ELECTOR PHOTO IDENTITY CARD|CARD|IDENTITY CARD)$')
    voter_no = voter_no[0]
    epic_no = voter_no.replace(" ", "")
    print('\n')
    print('Epic No:',epic_no)
    ##
    return data



def face_detect(filename):
    img=cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Original image', img)

    faces = face_classifier.detectMultiScale(gray, 1.3, 5)


    if faces is ():
        print("No faces found")


    for (x, y, w, h) in faces:
        x = x - 25 
        y = y - 40 
        cv2.rectangle(img, (x, y), (x + w + 50, y + h + 70), (27, 200, 10), 2)
        cv2.imshow('Face Detection', img)
        crop_img = img[y: y + h+70, x: x + w+50] 
        cv2.imwrite('/home/arijitsen/PAN-Card-OCR-master/media/Face2.jpg',crop_img)
        
        cv2.waitKey(1000)
    cv2.destroyAllWindows() 
    return crop_img




"""
def text_process():

    # Open and reading the textfile containing result
    filename = open('../TextExtract.txt', 'r')
    text = filename.read()

    text1 = []

    # Splitting the lines to sort the text paragraph wise
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    # Using regex to find the neceesary information
    def findword(textlist, wordstring):
        lineno = -1
        for wordline in textlist:
            xx = wordline.split()
            if ([w for w in xx if re.search(wordstring, w)]):
                lineno = textlist.index(wordline)
                textlist = textlist[lineno+1:]
                return textlist
        return textlist

    # Finding the electors number 
    voter_no = findword(text1, '(ELECTION COMMISSION OF INDIA ELECTORAL PHOTO IDENTITY CARD|CARD|IDENTITY CARD)$')
    voter_no = voter_no[0]
    epic_no = voter_no.replace(" ", "")
    print('\n')
    print('Epic No:',epic_no)

    # Some voter id's last name is printed on next line hence, it will extract from next line
    find_word = "(Elector's Name|NAME|Name)$"
    name_end = findword(text1, find_word)
    endname = name_end[0]

    lines = text
    for x in lines.split('\n'):
        _ = x.split()
        if ([w for w in _ if re.search("(Elector's Name|ELECTOR'S NAME|NAME|Name|name)$", w)]):
            person_name = x
            person_name = person_name.split(':')[1].strip()
            
            # If voter id's endname is on next line it will join it
            if endname:
                print("Elector's Name:",person_name + ' ' + endname)
                full_name = person_name + ' ' + endname
            else:
                print(person_name)
                full_name = person_name

        # Finding the father/husband/mother name        
        if ([w for w in _ if re.search("(Father's|Mother's|Husband's)$", w)]):
            elder_name = x
            elder_name = elder_name.split(':')[1].strip()
            print("Father's Name:",elder_name)
            
        # Finding the gender of the electoral candidate    
        if ([w for w in _ if re.search('(sex|SEX|Sex)$', w)]):
            gender = x
            gender = gender.split('/')
            sex = ''.join(gender[2]).strip()
            print('Sex:',sex)
        
        # Finding the Date of Birth 
        if ([w for w in _ if re.search('(Year|Birth|Date of Birth|DATE OF BIRTH|DOB)$', w)]):
            year = x
            year = year.split(':')
            dob = ''.join(year[1:]).strip()
            print('Date of Birth:',dob)

    # Converting the extracted informaton into json
    di = {'Epic No':epic_no,
        'Elector Name':full_name,
        'Father Name':elder_name
        #'Sex':sex,
        #'Date of Birth':dob
        }

    # Saving the json file
    print('\n',di)
    with open('../Result.json', 'w') as fp:
        json.dump(di, fp, sort_keys=True, indent=4)
    return di

    """