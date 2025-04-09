import logging
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from utils.permissions import IsOwner
from .models import User
from .serializers import CreateUserSerializer, UpdateRetrieveUserSerializer

logger = logging.getLogger('project')


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=TokenObtainPairSerializer,
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        operation_description="Login and get JWT token pair",
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Login attempt with email: {request.data.get('email')}")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Login successful for: {request.data.get('email')}")
        else:
            logger.warning(f"Login failed for: {request.data.get('email')}")
        response.status_code = 200
        return response


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Refresh the access token using a valid refresh token.",
        request_body=TokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Invalid or expired refresh token',
        },
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs) -> Response:
        logger.info("Access token refresh attempt")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info("Access token refreshed successfully")
        else:
            logger.warning("Access token refresh failed")
        response.status_code = 200
        return response


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
        email = kwargs.get('email')
        logger.info(f"User detail requested for: {email}")
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        email = kwargs.get('email')
        logger.info(f"User update attempt for: {email}")
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f"User updated successfully: {email}")
        return Response(serializer.data)
