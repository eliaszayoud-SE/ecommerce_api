import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['ecommerce-api-inht.onrender.com']

DATABASES = {
	"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'


CLOUDINARY_STORAGE = {
    'CLOUD_NAME':str(os.environ['CLOUD_NAME']),
    'API_KEY': str(os.environ['API_KEY']),
    'API_SECRET': str(os.environ['API_SECRET'])
}

print(type(os.environ['CLOUD_NAME']), os.environ['API_KEY'],os.environ['API_SECRET']  ) 