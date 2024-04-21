from pathlib import Path
from django.contrib.messages import constants
import os

MESSAGE_TAGS = {
    constants.DEBUG:    'alert-primary',
    constants.ERROR:    'alert-danger',
    constants.SUCCESS:  'alert-success',
    constants.INFO:     'alert-info',
    constants.WARNING:  'alert-warning',
}

BASE_DIR            = Path(__file__).resolve().parent.parent
STATIC_URL          = '/static/'
MEDIA_URL           = '/media/'
STATICFILES_DIRS    =(os.path.join(BASE_DIR, 'clinica/templates/static'),)
MEDIA_ROOT          = os.path.join(BASE_DIR, 'clinica/templates/media')
#STATIC_ROOT        = os.path.join('static')

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'apc.sqlite3', } }

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#+c)x$fnr&p$$is%s^p5vvst3&&e_bvrdog#xbmg@0*)%c)p%l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clinica',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'apc.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },
    {        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    },
    {        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    },
    {        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
