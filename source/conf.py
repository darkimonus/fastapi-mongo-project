from starlette.config import Config, environ
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

DEPLOYMENT_SERVER = config('DEPLOYMENT_SERVER')
MONGO_HOST = config('MONGO_HOST')
MONGO_PORT = config('MONGO_PORT')
MONGO_USER = config('MONGO_USER')
MONGO_PASS = config('MONGO_PASS')
MONGO_DB_NAME = config('MONGO_DB_NAME')
RESERVATION_BEFORE_AND_AFTER_TIME = config('RESERVATION_BEFORE_AND_AFTER_TIME')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default=['*'])

if environ.get('TESTING') == 'TRUE':
    database_name = f'test-{MONGO_DB_NAME}'
