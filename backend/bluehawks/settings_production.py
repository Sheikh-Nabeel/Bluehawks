"""
Production settings for bluehawks project.
"""

import os
import dj_database_url
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-36wy_+(ufvcp)5nm@0y-$-bn9%1931rz0pu_i4(m*m&+n@0s8p')

# Update allowed hosts for production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Where Django will look for static files you create manually
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../frontend/static'),
    os.path.join(BASE_DIR, 'static'),  # Backend static files (admin, etc.)
]

# Where Django will collect all static files (output folder for deployment)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for better static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings for Production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
} 