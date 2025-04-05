from django.urls import path
from .views import ListCreateEventView, JoinEventView

urlpatterns = [
    path('',ListCreateEventView.as_view({'get': 'list', 'post': 'create'}),name='event'),
    path('<int:pk>/<str:title>', ListCreateEventView.as_view({'get': 'retrieve', 'put': 'update'}), name='event-detail'),
    path('<int:event_id>/<str:title>/join', JoinEventView.as_view(), name="join-event" )
]
