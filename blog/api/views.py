from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.viewsets import ModelViewSet

from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.serializers import (PostDetailSerializer, PostSerializer,
                                  TagSerializer, UserSerializer)
from blog.models import Post, Tag
from blog_auth.models import User


class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
