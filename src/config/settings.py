from pathlib import Path
import os
import dj_database_url
import django
from decouple import config
from datetime import timedelta
from corsheaders.defaults import default_headers



DEBUG = config('DEBUG', default=True, cast=bool)
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='django-insecure-lb(#!ebof#o-ngp-izg12-nhy2@_jm@hs(^41mg!*oe7=9!m^t')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
AUTH_USER_MODEL = 'accounts.User'
QUERYDEBUG = False
# Application definition


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',


    #local
    'accounts.apps.AccountsConfig',
    'api.apps.ApiConfig',
    'docs.apps.DocsConfig',
    #

    #external
    'bootstrapform',
    'rest_framework',
    'corsheaders',
    'storages',
    'channels',
    'tinymce',
    'adminsortable2',
    'rest_framework_recursive',
    'drf_multiple_model',
    'drf_spectacular',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    #
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'config.custom_middleware.UpdateLastActiveMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
if QUERYDEBUG:
    MIDDLEWARE += ['django_query_profiler.client.middleware.QueryProfilerMiddleware',]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [

]



CORS_ALLOW_CREDENTIALS = True

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}



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
SITE_ID=1
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_PROVIDERS = {
    
}

LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'CET'

USE_I18N = True

USE_TZ = True

STATIC_URL = config('CDN_HOSTNAME', default='') + '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = config('CDN_HOSTNAME', default='') + '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ACCOUNT_USER_MODEL_USERNAME_FIELD = None


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 10,
    'ORDERING_PARAM': 'ordering',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/minute',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

BASE_URL = config('BASE_URL', default='')
MEDIA_URL_PREFIX = config('CDN_HOSTNAME', default='')
TRACKING_URL_PREFIX = config('TRACKING_URL_PREFIX', default='')
FRONT_URL_PREFIX = config('FRONT_URL_PREFIX', default='')
SPECTACULAR_SETTINGS = {
    'TITLE': 'finio App API',
    'DESCRIPTION': 'finio API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'SERVE_PUBLIC': True,
    'SERVE_URLCONF': 'config.urls',
    'SERVERS': [
        {
            'url': BASE_URL,
            'description': 'Server',
        },
    ],
    'SCHEMA_PATH_PREFIX': '/api',
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    # OTHER SETTINGS
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60 * 24),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=60 * 24 * 7),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'jwt_secret',
    'ALGORITHM': 'HS256',
}

# Documentation configuration
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'DISPLAY_OPERATION_ID': False,
    'OPERATIONS_SORTER': 'method',
    'SECURITY_DEFINITIONS': {
        'BearerToken': {
            'scheme': 'bearer',
            'type': 'https'
        }
    },
}
FRONT_HOSTNAME = config('FRONT_HOSTNAME', default='https://api-finio.truffel.dev')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6340/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6340/0')

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

CSRF_TRUSTED_ORIGINS = ['https://*.truffel.dev', 'https://*.api-finio.truffel.dev', 'https://*.finio.truffel.dev']




