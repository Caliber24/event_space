from django.urls import path
from .views import ListCreateEventView

urlpatterns = [
    path('',ListCreateEventView.as_view({'get': 'list', 'post': 'create'}),name='event'),
]
