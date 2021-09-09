from django import forms
from .models import ImageUploadModel
from .models import FileUploadModel


class UploadImageForm(forms.Form):
  #title = forms.CharField(max_length=50)
  #file = forms.FileField()
  image = forms.ImageField()


class ImageUploadForm(forms.ModelForm):
  class Meta:
    model = ImageUploadModel
    fields = ('image', )





class UploadFileForm(forms.ModelForm):
  class Meta:
    model = FileUploadModel
    fields = ('file', )