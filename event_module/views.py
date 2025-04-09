from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from utils.permissions import IsOwner

from .models import Event
from .serializers import (EventDetailSerializer, EventSerializer,
                          JoinEventSerializer)
from .services import event_service

# from rest_framework.permissions import
# Create your views here.


class ListCreateEventView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.prefetch_related('participants').filter(status=0)

    # def get_permissions(self):
    #     if self.action in ['create', 'retrieve', 'update', 'partial_update']:
    #         return [IsOwner()]
    #     else:
    #         return [IsAuthenticated()]

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
            data = {
                "error": 'این رویداد به اتمام رسیده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if event_status is False:
            data = {
                "error": 'این رویداد کنسل شده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_capacity_and_cancel(event):
            data = {
                "error": 'این رویداد بدلیل به حد نصاب نرسیدن(ده درصد ظرفیت ) ظرفیت کنسل شده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not event_service.check_capacity(event):
            data = {
                "error": 'ظرفیت رویداد پر شده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_creator(event, request.user):
            data = {
                'error': 'شما سازنده رویداد هستید'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if event_service.check_event_participant(event, request.user):
            data = {
                "error": "شما در این  رویداد عضو شده اید"
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        event_service.add_participant(event, request.user)

        data_to_serializer = {
            'event': event,
            'user': request.user
        }

        serializer = JoinEventSerializer(data=data_to_serializer)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=HTTP_200_OK)


class LeaveShowMyEventParticipant(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin , mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.prefetch_related('participants').filter(participants=self.request.user)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event_service.check_event_creator(event, request.user):
            data = {
                "error": 'شما سازنده رویداد هستید و نمیتوانید از آن خارج شوید'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if event_service.check_time_remaining_event(event):
            data = {
                'error': 'بدلیل اینکه 1 ساعت دیگر رویداد شروع میشود، نمیتوانید از رویداد خارج شوید'
            }

            return Response(data, status=HTTP_400_BAD_REQUEST)

        event_service.remove_participant(event, request.user)
        data = {
            'data': 'شما از رویداد خارج شدید'
        }
        return Response(data, status=HTTP_200_OK)


class CancelledShowMyEventCreate(GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = []
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.prefetch_related('participants').filter(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        event_status = event_service.check_status_event(event)
        if event_status is True:
            data = {
                "error": 'این رویداد به اتمام رسیده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not event_status:
            data = {
                'error': 'این رویداد از پیش کنسل شده است'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if not event_service.check_capacity(event):
            data = {
                "error": ' ظرفیت رویداد پر شده است و شما نمیتوانید کنسل کنید'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        
        if event_service.check_time_remaining_event(event):
            data = {
                'error': 'بدلیل اینکه 1 ساعت دیگر رویداد شروع میشود، نمیتوانید از رویداد را کنسل کنید.'
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        
        event.delete()
        data = {
            'data': 'شما رویداد را کنسل کردید'
        }
        return Response(data, status=HTTP_200_OK)
