from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.permissions import CurrentUserOrAdmin
from djoser.serializers import SetPasswordSerializer
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          SubscribeSerializer)

User = get_user_model()


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    permission_classes = [CurrentUserOrAdmin, ]
    filter_backends = [DjangoFilterBackend, ]
    lookup_field = 'id'

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'subscriptions':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'me':
            return CustomUserSerializer
        elif self.action == 'create':
            return CustomUserCreateSerializer
        elif self.action == 'subscriptions':
            return SubscribeSerializer
        return self.serializer_class

    @action(
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def subscriptions(self, request):
        following = Follow.objects.filter(user=request.user).order_by('author')
        queryset = [
            User.objects.get(id=author.author.id)
            for author in following
        ]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get', 'delete'],
        detail=True)
    def subscribe(self, request, id):
        if request.method == 'GET':
            if request.user == get_object_or_404(User, id=id):
                return Response(
                    {'error': 'Вы не можете подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow_check = Follow.objects.filter(
                user=request.user,
                author=get_object_or_404(User, id=id))
            if follow_check.exists():
                return Response(
                    {'error': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST)

            Follow.objects.create(
                user=request.user,
                author=get_object_or_404(User, id=id)
            )
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = Follow.objects.filter(
                user=request.user,
                author=get_object_or_404(User, id=id))
            if follow.exists() is False:
                return Response(
                    {'error': 'Вы не можете отписаться не создав подписку'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = SubscribeSerializer(data=request.data)
        return Response(serializer, status=status.HTTP_200_OK)
