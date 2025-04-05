from django.shortcuts import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from utils.permissions import IsOwner

from .models import User
from .serializers import CreateUserSerializer, UpdateRetrieveUserSerializer

# Create your views here.


class CreateRetrieveUpdateUserViewset(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UpdateRetrieveUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        else:
            return [IsOwner()]

    def retrieve(self, request, *args, **kwargs):
        email = kwargs.get('ema1il')
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        email = kwargs.get('email')
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
