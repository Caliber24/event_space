from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Event
from .serializers import EventSerializer

# Create your views here.


class ListCreateEventView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    # def perform_create(self, serializer):
    #     if self.request.user :
    #         serializer.save(creator=self.request.user)


    