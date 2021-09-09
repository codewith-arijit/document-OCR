from django.conf.urls import url 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.first_view, name='first_view'),
    url(r'^uimage/$', views.uimage, name='uimage'), #image upload template!
    url(r'^pancard/$', views.ocr_core, name='PanCard'), #PAN Card OCR template!
    url(r'^index', views.index, name='index'),
    url(r'^aadhar/$', views.aadhar, name='aadhar'),
    url(r'^voterid/$', views.voter_id, name='voterid'),
    url(r'^bank_id/$', views.bank_id, name='bank_id'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

