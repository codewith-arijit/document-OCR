import pytesseract
import cv2
import re

import cv2

from PIL import Image
import numpy as np
import regex

def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


def driver_license(filename):
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

    txt = pytesseract.image_to_string(i)
    print(txt)
    """
    for key in ('Issue Date', 'Licence No\.', 'N', 'Validity\(NT\)'):
        print(regex.findall(fr"(?<={'Licence No'}\s*:\s*)\b[^\n]+", txt, regex.IGNORECASE))
    """
    text = []
    data = {
        'firstName': None,
        'lastName': None,
        'documentNumber': None,
    }

    c = 0
    print(txt)
    pattern = "(?<=KEY\s*:\s*)\b[^\n]+"
    #Splitting lines
    lines = txt.split('\n')

    for lin in lines:
        c = c + 1
        s = lin.strip()
        s = s.replace('\n','')
        if s:
            s = s.rstrip()
            s = s.lstrip()
            text.append(s)

            try:
                if re.match(r".*Name|.*name|.*NAME", s):
                    name = re.sub('[^a-zA-Z]+', ' ', s)
                    name = name.replace('Name', '')
                    name = name.replace('name', '')
                    name = name.replace('NAME', '')
                    name = name.replace(':', '')
                    name = name.rstrip()
                    name = name.lstrip()
                    nmlt = name.split(" ")
                    data['firstName'] = " ".join(nmlt[:len(nmlt)-1])
                    data['lastName'] = nmlt[-1]
                if re.search(r"[a-zA-Z][a-zA-Z]-\d{13}", s):
                    data['documentNumber'] = re.search(r'[a-zA-Z][a-zA-Z]-\d{13}', s)
                    data['documentNumber'] = data['documentNumber'].group().replace('-', '')
                    if not data['firstName']:
                        name = lines[c]
                        name = re.sub('[^a-zA-Z]+', ' ', name)
                        name = name.rstrip()
                        name = name.lstrip()
                        nmlt = name.split(" ")
                        data['firstName'] = " ".join(nmlt[:len(nmlt)-1])
                        data['lastName'] = nmlt[-1]
                if re.search(r"[a-zA-Z][a-zA-Z]\d{2} \d{11}", s):
                    data['documentNumber'] = re.search(r'[a-zA-Z][a-zA-Z]\d{2} \d{11}', s)
                    data['documentNumber'] = data['documentNumber'].group().replace(' ', '')
                    if not data['firstName']:
                        name = lines[c]
                        name = re.sub('[^a-zA-Z]+', ' ', name)
                        name = name.rstrip()
                        name = name.lstrip()
                        nmlt = name.split(" ")
                        data['firstName'] = " ".join(nmlt[:len(nmlt)-1])
                        data['lastName'] = nmlt[-1]
                """
                if re.match(r".*DOB|.*dob|.*Dob", s):
                    yob = re.sub('[^0-9]+', ' ', s)
                    yob = re.search(r'\d\d\d\d', yob)
                    data['age'] = datetime.datetime.now().year - int(yob.group())
                    """
            except:
                pass
    #new_data = Convert(data)
    #print(new_data)
    list_data = [data['firstName'], data['lastName'], data['documentNumber']]
    return list_data #data

