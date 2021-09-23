from api.models import PanCard
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import PanCardView, PanCardViewDetails 
#import PanCardView, PanCardViewDetails

urlpatterns = [
    path('api/v1/', views.PanCardView.as_view()),
    path('api/v1/<int:pk>', views.PanCardViewDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)