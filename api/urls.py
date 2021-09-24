from api.models import PanCard
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import PanCardView #, PanCardViewDetails 
#import PanCardView, PanCardViewDetails

urlpatterns = [
    path('api/v1/pancard', views.PanCardView),
    #path('api/v1/upload/<int:pk>', views.PanCardViewDetails),
]

urlpatterns = format_suffix_patterns(urlpatterns)