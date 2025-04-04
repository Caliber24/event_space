from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Event
from .serializers import EventSerializer
# from rest_framework.permissions import 
# Create your views here.


class ListCreateEventView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    
    # def get_permissions(self):
        
    
    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user)
