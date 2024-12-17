from celery import Celery
from conf import config

CELERY_NAME = config.get('CELERY_NAME')
REDIS_HOST = config.get("REDIS_HOST", default='localhost')
REDIS_PORT = config.get('REDIS_PORT', default='6379')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

celery_app = Celery(CELERY_NAME, broker=REDIS_URL)

celery_app.conf.update(
    result_backend=REDIS_URL,
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
