from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.serializers import (PostDetailSerializer, PostSerializer,
                                  TagSerializer, UserSerializer)
from blog.models import Post, Tag
from blog_auth.models import User


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return PostSerializer
        return PostDetailSerializer


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
