from celery import Celery
from conf import settings

CELERY_NAME = settings.celery.celery_name
REDIS_HOST = settings.redis.redis_host
REDIS_PORT = settings.redis.redis_port
REDIS_PASSWORD = settings.redis.redis_password
if REDIS_PASSWORD:
    REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
else:
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

celery_app = Celery(CELERY_NAME, broker=REDIS_URL)

celery_app.conf.update(
    result_backend=REDIS_URL,
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
