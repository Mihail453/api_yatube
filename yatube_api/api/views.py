from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Автоматически заполняем поле author."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение для групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAuthorOrReadOnly]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Получаем комментарии только для нужного поста."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """Автоматически заполняем author и post."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
