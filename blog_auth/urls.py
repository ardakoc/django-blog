from django.urls import include, path
from django_registration.backends.activation.views import RegistrationView

from blog import views
from blog_auth.forms import BlogRegistrationForm

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path(
        'register/',
        RegistrationView.as_view(form_class=BlogRegistrationForm),
        name='django_registration_register'
    )
]