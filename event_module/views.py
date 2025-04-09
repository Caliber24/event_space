from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_202_ACCEPTED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from utils.permissions import IsOwner
from .filters import EventFilter
from .models import Event
from .serializers import (ChangeStatusEventSerializer, EventDetailSerializer,
                          EventSerializer, JoinEventSerializer)
from .services import event_service


class ListCreateEventView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title','description','creator__email']
    ordering_fields = ['start_date', 'title','price']
    def get_queryset(self):
        return Event.objects.filter(status=0).prefetch_related('participants')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'list':
            return []
        return [IsOwner()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        else:
            return EventSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


class JoinEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        event_status = event_service.check_status_event(event)
        if event_status is True:
            return Response({"error": "This event has ended."}, status=HTTP_400_BAD_REQUEST)
        if event_status is False:
            return Response({"error": "This event has been canceled."}, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_capacity_and_cancel(event):
            return Response({"error": "This event was canceled due to insufficient capacity."},
                            status=HTTP_400_BAD_REQUEST)
        if not event_service.check_capacity(event):
            return Response({"error": "The event is full."}, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_creator(event, request.user):
            return Response({"error": "You are the creator of this event."}, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_participant(event, request.user):
            return Response({"error": "You are already a participant in this event."}, status=HTTP_400_BAD_REQUEST)

        event_service.add_participant(event, request.user)

        data_to_serializer = {
            'event': event,
            'user': request.user
        }

        serializer = JoinEventSerializer(data=data_to_serializer)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=HTTP_200_OK)


class LeaveShowMyEventParticipant(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['start_date', 'title', 'price']
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Event.objects.none()

        if self.request.user.is_authenticated:
            queryset = Event.objects.filter(participants=self.request.user)
            return queryset.prefetch_related('participants')
        return Event.objects.none()


class ChangeStatusShowMyEventCreate(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeStatusEventSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['start_date', 'title', 'price']
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Event.objects.none()

        if self.request.user.is_authenticated:
            queryset = Event.objects.filter(creator=self.request.user)
            return queryset.prefetch_related('participants')
        return Event.objects.none()

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        event_status = event_service.check_status_event(event)
        if event_status is True:
            return Response({"error": "This event has ended."}, status=HTTP_400_BAD_REQUEST)

        if event_status is False:
            return Response({"error": "This event has been canceled."}, status=HTTP_400_BAD_REQUEST)

        event_status = int(request.data.get('status'))
        if event_status == 1:
            if not event_service.check_time_after_start_date(event):
                return Response({"error": "This event has not started yet."}, status=HTTP_400_BAD_REQUEST)
            event.status = 1
            serializer = self.get_serializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)

        if event_status == 2:
            if not event_service.check_capacity(event):
                return Response({"error": "The event is full and cannot be canceled."}, status=HTTP_400_BAD_REQUEST)

            event.status = 2
            serializer = self.get_serializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)

        return Response({'error': 'Invalid input'}, status=HTTP_200_OK)
