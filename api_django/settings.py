"""
Django settings for api_django project.
"""

from pathlib import Path
import os, dj_database_url

# =========================
# BASE
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tu-clave-secreta-aqui-123456'
DEBUG = True

# =========================
# ALLOWED HOSTS
# =========================
ALLOWED_HOSTS = [
    "yamanote.proxy.rlwy.net", 
    "localhost",
    "127.0.0.1", 
    "0.0.0.0",
    "condominio-jht3.onrender.com",
    "condominio-psi.vercel.app",
]

STRIPE_SECRET_KEY = "sk_test_51RRklm4Zqdn7RVeShGNEhW7wo7nVUDZRenO3u5gRLtuygmV2iCzWB0OdPB6YxF8pYwqVSww887vkhE6GXgHfJw2Z00yWO4QYsY"
STRIPE_PUBLIC_KEY = "pk_test_51RRklm4Zqdn7RVeS6rpZkRzHEQb5ZsZ3ud3Lj7SdElZskhVK0c2kbzXX7OHRDbriJ4u1MBNriwpPXUB89lS9LHi900U2jWD6it"

# =========================
# INSTALLED APPS (SIMPLIFICADO)
# =========================
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INSTALLED_APPS = [
        'corsheaders',  # ✅ SOLO el nombre de la app aquí
    

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colegio',
    'rest_framework',
    'stripe',
]

# =========================
# MIDDLEWARE (SIMPLIFICADO)
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # ✅ MOVE the MIDDLEWARE here
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://condominio-psi.vercel.app",
    "http://127.0.0.1:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
# =========================
# URLS Y TEMPLATES
# =========================
ROOT_URLCONF = 'api_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_django.wsgi.application'

# =========================
# BASE DE DATOS - ORIGINAL (SQLite3)
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',  # PGDATABASE / POSTGRES_DB
        'USER': 'postgres',  # PGUSER / POSTGRES_USER
        'PASSWORD': 'uxnyEwIttCQflQOMInHvxezYnAZfvaDE',  # PGPASSWORD / POSTGRES_PASSWORD
        'HOST': 'yamanote.proxy.rlwy.net',  # DATABASE_PUBLIC_URL host
        'PORT': '52824',  # DATABASE_PUBLIC_URL port
    }
}

# =========================
# VALIDADORES DE CONTRASEÑA
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# LOCALIZACIÓN
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =========================
# AUTO FIELD
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Agrega al FINAL del archivo settings.py:
CORS_ALLOW_ALL_ORIGINS = True  # Para desarrollo (en producción especifica los dominios)
CORS_ALLOW_CREDENTIALS = True
