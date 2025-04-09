from django.urls import path
from .views import ListCreateEventView, JoinEventView, LeaveShowMyEventParticipant, ChangeStatusShowMyEventCreate

urlpatterns = [
    path('',ListCreateEventView.as_view({'get': 'list', 'post': 'create'}),name='event'),
    path('<int:pk>/', ListCreateEventView.as_view({'get': 'retrieve', 'put': 'partial_update'}), name='event-detail'),
    path('<int:event_id>/join', JoinEventView.as_view(), name="join-event" ),
    path('my-event-participant', LeaveShowMyEventParticipant.as_view({'get': 'list'}),name='list-my-event-participant'),
    path('my-event-participant/<int:pk>/remove', LeaveShowMyEventParticipant.as_view({'get':'retrieve' , 'delete': 'destroy'}), name='leave-event'),
    path('my-event-create', ChangeStatusShowMyEventCreate.as_view({'get':'list'}), name='my-event-create'),
    path('my-event-create/<int:pk>', ChangeStatusShowMyEventCreate.as_view({'get':'retrieve', 'put': 'update'}), name='my-event-create'),
    
]
