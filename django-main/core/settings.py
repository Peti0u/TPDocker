# -*- encoding: utf-8 -*-
"""
Copyright (c) AppSeed.us
"""

import os, random, string
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b+$5wugqo%4&wt1+^jy+6x+#p3z*f__c__7(j9-4qp@24nl65n"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts Settings
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5085",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5085",
    "https://dynamic-django.onrender.com",
]

# Application definition

INSTALLED_APPS = [
    "admin_berry_pro.apps.AdminBerryProConfig",    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
    "debug_toolbar",
    "django_dyn_api",
    "django_dyn_dt",
    "django_dyn_charts",
    "admin_berry.apps.AdminBerryConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "dbbackup",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

UI_TEMPLATES = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [UI_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "home.context_processors.get_settings",
                "home.context_processors.analytics_key",                
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_ENGINE   = os.environ.get('DB_ENGINE')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASS     = os.environ.get('DB_PASS')
DB_HOST     = os.environ.get('DB_HOST')
DB_PORT     = os.environ.get('DB_PORT')
DB_NAME     = os.environ.get('DB_NAME')

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = { 
        'default': {
            'ENGINE'  : 'django.db.backends.' + DB_ENGINE, 
            'NAME'    : DB_NAME,
            'USER'    : DB_USERNAME,
            'PASSWORD': DB_PASS,
            'HOST'    : DB_HOST,
            'PORT'    : DB_PORT,
        },          
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "/"
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

# Syntax: URI -> Import_PATH
DYNAMIC_API = {
    "product": "home.models.Product",
    "sales": "home.models.Sales",
}

# Syntax: URI -> Import_PATH
DYNAMIC_DATATB = {
    "product": "home.models.Product",
    "sales": "home.models.Sales",
    "titanic": "home.models.Titanic",
}

# Syntax: URI -> Import_PATH
DYNAMIC_CHARTS = {
    "product": "home.models.Product",
    "sales": "home.models.Sales",
    "titanic": "home.models.Titanic",
} 

# AI Interface 
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# DB BackUp/Restore
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'db-backup'}

# Analytics 
GOOGLE_ANALYTICS_KEY=os.getenv('GOOGLE_ANALYTICS_KEY')
