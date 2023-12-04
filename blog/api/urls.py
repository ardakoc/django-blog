from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import PostDetailAPIView, PostListAPIView, UserDetailAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('users/<str:email>', UserDetailAPIView.as_view(), name='api_user_detail'),
    # authentication
    path('auth/', include('rest_framework.urls')),
    path('token-auth/', views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)