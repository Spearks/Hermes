"""
Django settings for hermes project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'cacheops',
    'widget_tweaks',
    'rest_framework',
    'django_extensions',
    'django_minify_html',
    # Hermes Web-Ui
    'app',
    # Hermes API
    'api'
    # Hermes accounts

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_minify_html.middleware.MinifyHtmlMiddleware'
]

ROOT_URLCONF = 'hermes.urls'
LOGIN_REDIRECT_URL = "/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'hermes.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#'django_psdb_engine',
        'NAME': env('PSQL_DB_NAME'),
        'USER': env('PSQL_DB_USER'),
        'PASSWORD': env('PSQL_DB_PASSWORD'),
        'HOST': env('PSQL_DB_HOST'),
        'PORT': env('PSQL_DB_PORT'),
        #'OPTIONS': {'ssl': {'ca': env('MYSQL_ATTR_SSL_CA')}}
    }
}

GRAFANAHOST = env('GRAFANAHOST')
GRAFANAPORT= env('GRAFANAPORT')

PROMETHEUS_HOST = env('PROMETHEUS_HOST')
PROMETHEUS_PORT = env('PROMETHEUS_PORT')

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIMEZONE')

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticroot')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static/staticroot'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
MEDIA_ROOT = (
  os.path.join(BASE_DIR, 'media')
)
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Config
CELERY_TIMEZONE = env('TIMEZONE')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_RESULT_EXPIRES = 1800
CELERY_RESULT_BACKEND = env('REDIS_CELERY_RESULT_BACKEND')
#CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
#CELERY_TASK_ALWAYS_EAGER = True

CELERY_BEAT_SCHEDULE = {
    'dashboard-auto-update': {
        'task': 'app.tasks.update_dashboard',
        'schedule': 10,  # Update dashboards 
    },
}

# Compressor config
COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

LOGIN_URL = 'accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = "/"

# Cache-ops config 
CACHEOPS_REDIS = {
    'host': env('REDIS_HOST'),
    'port': env('REDIS_PORT'),       
    'db': 3,           
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60*10},

    # Cache all queries to Permission
    # 'all' is an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    'auth.permission': {'ops': 'all', 'timeout': 60*10},

    'app.*': {'ops': {'fetch', 'get', 'count'}, 'timeout': 60*10},
}
CACHEOPS_DEGRADE_ON_FAILURE = True

# Django rest-framework configs
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}