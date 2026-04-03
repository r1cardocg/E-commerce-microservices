import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY  = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key')
DEBUG       = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'usuarios',
]

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME', 'usuarios_db'),
        'USER':     os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST':     os.getenv('DB_HOST', '127.0.0.1'),
        'PORT':     os.getenv('DB_PORT', '5432'),
    }
}

ROOT_URLCONF       = 'urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ             = True
TIME_ZONE          = 'UTC'