"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l9pp-e-%%mvu*namelukv!(5$awz35+vjve@#0=xig0%y+^!zt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
	}
# Application definition

INSTALLED_APPS = [
	# Jia <new pkg>: TODO install on BPlatform
	'crispy_forms',
	'django_tables2',
	########
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'analyzer.apps.AnalyzerConfig',
    #'issue_import.apps.apps.IssueImportConfig',
	#'notification.apps.NotificationConfig',
	'userconfig.apps.UserconfigConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'userconfig.middleware.healthcheck.HealthCheckMiddleware',
]

ROOT_URLCONF = 'apps.urls'

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

WSGI_APPLICATION = 'apps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Notes:
# On BPlatform directly import mysql database to django models:
# python3 manage.py inspectdb > yourapp/models.py will work:

DATABASES = {

	## localhost databse 
 #   'default': {
 #       'NAME': 'qa',
 #       'ENGINE': 'django.db.backends.mysql',
 #       'USER': 'django',
 #       'PASSWORD': '123456',
 #       'HOST':'localhost',
 #       'PORT':'3306',
 #   }
 	# BPlatform databse 
 	   'default': {
 	       'NAME': 'chinaqa',
 	       'ENGINE': 'django.db.backends.mysql',
 	       'USER': 'crashmonitorbotfire_chinaqa_rw0',
 	       'PASSWORD': 'Ugzdq7E3PDzJ1wBp',
 	       'HOST':'dev-inttoolmdb-vip.lhr4.dqs.booking.com',
 	       'PORT':'3306',
			'OPTIONS': {
            'connect_timeout': 5,
        }

 	   }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
