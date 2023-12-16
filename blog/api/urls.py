from django.urls import include, path, re_path
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import (PostDetailAPIView, PostListAPIView,
                            UserDetailAPIView)
from blog.api.schema.views import schema_view

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('users/<str:email>', UserDetailAPIView.as_view(), name='api_user_detail'),
    # authentication
    path('auth/', include('rest_framework.urls')),
    path('token-auth/', views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# documentation
urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
]
