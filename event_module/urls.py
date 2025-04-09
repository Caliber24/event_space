from django.urls import path
from .views import ListCreateEventView, JoinEventView, LeaveShowMyEventParticipant, CancelledShowMyEventCreate

urlpatterns = [
    path('',ListCreateEventView.as_view({'get': 'list', 'post': 'create'}),name='event'),
    path('<int:pk>/<str:title>', ListCreateEventView.as_view({'get': 'retrieve', 'put': 'update'}), name='event-detail'),
    path('<int:event_id>/join', JoinEventView.as_view(), name="join-event" ),
    path('my-event-participant', LeaveShowMyEventParticipant.as_view({'get': 'list'}),name='list-my-event-participant'),
    path('my-event-participant/<int:pk>/remove', LeaveShowMyEventParticipant.as_view({'get':'retrieve' , 'delete': 'destroy'}), name='leave-event'),
    path('my-event-create', CancelledShowMyEventCreate.as_view({'get':'list'}), name='my-event-create'),
]
