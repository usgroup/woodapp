from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

__all__ = ['ALLOWED_HOSTS',"DATABASES"]