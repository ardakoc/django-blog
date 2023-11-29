from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import PostDetailAPIView, PostListAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)