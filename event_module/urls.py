from django.urls import path
from .views import ListCreateEventView

urlpatterns = [
    path('',ListCreateEventView.as_view({'get': 'list', 'post': 'create'}),name='event'),
    path('<int:pk>/<str:title>', ListCreateEventView.as_view({'get': 'retrieve', 'put': 'update'}), name='event-detail'),
]
