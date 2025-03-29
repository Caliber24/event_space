from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Event
from .serializers import EventSerializer

# Create your views here.


class ListCreateEventView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user) 


    