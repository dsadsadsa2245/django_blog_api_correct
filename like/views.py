from django.shortcuts import render
from rest_framework import generics, permissions
from . import serializers
from .models import Like
# удалять лайки модет только автор
from posts.permissions import IsAuthor


class LIkeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (IsAuthor,)