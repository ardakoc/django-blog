from datetime import timedelta

from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.api.filters import PostFilterSet
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.serializers import (PostDetailSerializer, PostSerializer,
                                  TagSerializer, UserSerializer)
from blog.models import Post, Tag
from blog_auth.models import User


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    filterset_class = PostFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return PostSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            # published posts only
            queryset = self.queryset.filter(published_at__lte=timezone.now())
        elif self.request.user.is_staff:
            # all posts
            queryset = self.queryset
        else:
            # published or own posts
            queryset = self.queryset.filter(
                Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
            )
        
        time_period_name = self.kwargs.get('period_name')

        if not time_period_name:
            # no further filtering required
            return queryset
        
        if time_period_name == 'new':
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(hours=1)
            )
        elif time_period_name == 'today':
            return queryset.filter(
                published_at__date=timezone.now().date()
            )
        elif time_period_name == 'week':
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(days=7)
            )
        else:
            raise Http404(
                f'Time period {time_period_name} is not valid. '
                f'It should be "new", "today", or "week".'
            )
    
    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers('Authorization'))
    @method_decorator(vary_on_cookie)
    @action(methods=['get'], detail=False, name='Posts by the logged in user')
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied(
                'You must be logged in to see which posts are yours.'
            )

        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers('Authorization'))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    @method_decorator(cache_page(300))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=['get'], detail=True, name='Posts with the Tag')
    def posts(self, request, pk=None):
        tag = self.get_object()
        page = self.paginate_queryset(tag.posts.all())

        if page is not None:
            post_serializer = PostSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(post_serializer.data)

        post_serializer = PostSerializer(
            tag.posts, many=True, context={'request': request}
        )
        return Response(post_serializer.data)

    @method_decorator(cache_page(120))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
