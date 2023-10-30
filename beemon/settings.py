import os
import sys
from pathlib import Path
from loguru import logger
from decouple import config, Csv


BASE_DIR = Path(__file__).resolve().parent.parent

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")

DEBUG = config('DEBUG', default=False, cast=bool)

# Pega o ambiente atual
DJANGO_ENVIRONMENT = config('DJANGO_ENVIRONMENT')

# Se o ambiente é 'prod', usa a URL de produção. Caso contrário, usa a URL de QA.
if DJANGO_ENVIRONMENT == 'prod':
    CELERY_BROKER_URL = config('CELERY_BROKER_URL_PROD')
    CSRF_TRUSTED_ORIGINS = ['https://beemon.com.br']
    SCHEMA_DB = config("SCHEMA_DB_PROD")
else:
    CELERY_BROKER_URL = config('CELERY_BROKER_URL_QA')
    CSRF_TRUSTED_ORIGINS = ['https://beemon-qa.com.br']
    SCHEMA_DB = config("SCHEMA_DB_QA")
    
# Sempre deixara URL principal em primeiro lugar se for utilizar
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

APPS_DIR = sys.path.append(os.path.join(BASE_DIR, 'apps'))
DJANGO_APPS = [
    'jet',
    'jet.dashboard', 
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'import_export',
    'django_celery_beat',
    'django_celery_results',
]

# New apps added
PROJECT_APPS = [
    'core',
    'accounts',
    'data_scrapy'
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware'
]


SITE_ID = 1
LOGIN_URL = "accounts:login"
X_FRAME_OPTIONS = 'SAMEORIGIN'
AUTH_USER_MODEL = 'accounts.User'
IMPORT_EXPORT_USE_TRANSACTIONS = True 

# Quantidade de items para remover pelo django admin
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

ROOT_URLCONF = 'beemon.urls'


JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#333',
        'title': 'Light Gray'
    }
]
JET_DEFAULT_THEME = 'default'  # Nome do tema padrão



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.notification_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'beemon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path=beemondb,{SCHEMA_DB}',  # Substitua 'beemondb' pelo nome do esquema desejado
        },
    }
}

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

if DEBUG == False:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

#CONN celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_TASK_TRACK_STARTED = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
