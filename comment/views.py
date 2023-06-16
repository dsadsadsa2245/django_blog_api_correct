from django.shortcuts import render
from rest_framework import generics, permissions
from posts.permissions import IsAuthor, IsAuthorOrAdminOrPostOwner
from .models import Comment
from . import serializers


class CommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthorOrAdminOrPostOwner]
        return [permissions.AllowAny(), ]
