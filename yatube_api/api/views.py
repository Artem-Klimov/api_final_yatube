from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post
from rest_framework import mixins, pagination, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from .permissions import OwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                        PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('following__username', 'user__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
