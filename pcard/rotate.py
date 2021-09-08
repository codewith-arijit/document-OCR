from PIL import Image
from numpy.lib.type_check import imag
import pytesseract


imagepath = "/home/arijitsen/Downloads/PAN-Card-OCR/ro3.jpg"
def getImageOrientation(image):
    try:
        orientation = str(pytesseract.image_to_osd(image)).split('\n')[1].split(':')[1]
        return orientation
    except pytesseract.pytesseract.TesseractError:  #Exception occurs on empty pages, return 0 orientation
        return 0
          
def fixOrientation(image):
    orientation = getImageOrientation(image)
    rotated = image
    if(orientation!=0):
      rotated = image.rotate(360-int(orientation))
    return rotated
          
def convert(imagepath):
    image = Image.open(imagepath)
    image = image.convert("RGBA")

    rotated = fixOrientation(image)   #fix image orientation
    text = pytesseract.image_to_string(rotated, config='--psm 6')   #this config helps to read row by row

    print(text)

convert(imagepath)