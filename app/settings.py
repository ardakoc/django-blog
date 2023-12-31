"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from configurations import Configuration, values


class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-w2-tbnk^@*6^c8$=-!_!0%64a0zz86l1e6d0%ui@@%6ix9=rv*'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = INTERNAL_IPS = values.ListValue(['localhost', '0.0.0.0', '127.0.0.1'])

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.sites',
        'django.contrib.staticfiles',

        'blog',
        'blog_auth',

        'crispy_forms',
        'crispy_bootstrap5',
        'debug_toolbar',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'rest_framework',
        'rest_framework.authtoken',
        'drf_yasg',
        'django_filters',
        'versatileimagefield',
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'allauth.account.middleware.AccountMiddleware',
    ]

    ROOT_URLCONF = 'app.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'app.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

    DATABASES = values.DatabaseURLValue(f'sqlite:///{BASE_DIR}/db.sqlite3')


    # Password validation
    # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = values.Value('Europe/Istanbul')

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/

    STATIC_URL = 'static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

    CRISPY_TEMPLATE_PACK = 'bootstrap5'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.ScryptPasswordHasher',
    ]

    AUTH_USER_MODEL = 'blog_auth.User'

    LOGOUT_REDIRECT_URL = '/'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ACCOUNT_ACTIVATION_DAYS = 3
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None # There is no username field on the User model.
    ACCOUNT_EMAIL_REQUIRED = True # The third-party provider must provide an email address when authenticating.
    ACCOUNT_USERNAME_REQUIRED = False # The username of the User is not required.
    ACCOUNT_AUTHENTICATION_METHOD = 'email' # The user authenticates by entering their email address.

    SITE_ID = 1

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ],
        'DEFAULT_THROTTLE_CLASSES': [
            'blog.api.throttling.AnonSustainedThrottle',
            'blog.api.throttling.AnonBurstThrottle',
            'blog.api.throttling.UserSustainedThrottle',
            'blog.api.throttling.UserBurstThrottle',
        ],
        'DEFAULT_THROTTLE_RATES': {
            'anon_sustained': '500/day',
            'anon_burst': '10/minute',
            'user_sustained': '5000/day',
            'user_burst': '100/minute',
            'post_api': '50/minute',
            'user_api': '2000/day',
        },
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.OrderingFilter',
        ],
    }

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Token': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
            'Basic': {'type': 'basic'},
        }
    }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    }

    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'


class Prod(Dev):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
