from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, ]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'me':
            return CustomUserSerializer
        elif self.action == 'create':
            return CustomUserCreateSerializer
        elif self.action == 'subscriptions' or self.action == 'subscribe':
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
        self.request.user.set_password(
            serializer.validated_data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['GET', 'DELETE'],
        detail=True)
    def subscribe(self, request, id):
        if request.method == 'GET':
            author = get_object_or_404(User, id=id)
            if request.user == author:
                return Response(
                    {'error': 'Вы не можете подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow_check = Follow.objects.filter(
                user=request.user,
                author=author)
            if follow_check.exists():
                return Response(
                    {'error': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(
                user=request.user,
                author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            follow = Follow.objects.filter(
                user=request.user,
                author=get_object_or_404(User, id=id))
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Вы не можете отписаться не создав подписку'},
                status=status.HTTP_400_BAD_REQUEST)
