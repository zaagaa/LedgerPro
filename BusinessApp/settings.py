from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-qgnphi+(igh$np*hrdlsy9eb59_4b^i^y7&116dp^70w@*6up^'

DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Project apps
    'invoice.apps.InvoiceConfig',
    'BusinessApp',
    'frontend',
    'bootstrap5',
    'authentication',
    'inventory',
    'company',
    'dashboard',
    'attribute',
    'purchase',
    'supplier',
    'setting',
    'pos',
    'tax_code',
    'customer',
    'expenses',
    'bank',
    'sync',
    'todo',
    'staff',
    'qr_code',
    'statement',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'BusinessApp.middleware.SimpleMiddleware',
    'BusinessApp.middleware.UserActivityMiddleware',
    'BusinessApp.middleware.AutoLockMiddleware',
'BusinessApp.middleware.PageLoadTimeMiddleware',
'setting.middleware.SettingMiddleware',
    'pos.middleware.AutoDeleteUnprintedLogMiddleware',

]

ROOT_URLCONF = 'BusinessApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template dirs if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'BusinessApp.context_processors.context_processor',
                'authentication.context_processors.impersonation_flag',
                'BusinessApp.context_processors.version_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'BusinessApp.wsgi.application'




DB_CONFIG_PATH = os.path.join(BASE_DIR, 'db_config.json')

if os.path.exists(DB_CONFIG_PATH):
    with open(DB_CONFIG_PATH) as f:
        DATABASES = {
            'default': json.load(f)
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }



# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Timezone and language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ Add this

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Custom constants
API_URL = "https://zaagaa.pythonanywhere.com"

# Default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


with open(os.path.join(BASE_DIR, 'version.txt')) as f:
    VERSION = f.read().strip()
    # print(VERSION,"VERSION")