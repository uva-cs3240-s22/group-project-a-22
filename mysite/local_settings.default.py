# This is a default local settings file
# Copy this file, rename it local_settings.py, and change the specified settings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ''  # add your django secret key here

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
