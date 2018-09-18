# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

from authors.settings.base import *

from urllib.parse import urlparse

db_url = os.getenv("TEST_DATABASE_URL")

parsed_url = urlparse(db_url)

dbname = parsed_url.path[1:]
username = parsed_url.username
hostname = parsed_url.hostname
pwd = parsed_url.password
port_number = parsed_url.port

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'authors_haven_test',
        'USER': 'postgres',
        'PASSWORD': 'RIp0772466608*',
        'HOST': hostname,
        'PORT': port_number,
    }
}
