#!/bin/bash
set -e
if [ "$CONTAINER_TYPE" = "master" ]; then
    if [ "$DEPLOYMENT_SERVER" = "False" ]; then
    poetry run uvicorn main:app --host 0.0.0.0 --port 8000
    fi
fi

if [ "$CONTAINER_TYPE" = "worker" ]; then
    poetry run celery -A celery_app worker -l info -Q restaurants_queue --concurrency=3
fi

if [ "$CONTAINER_TYPE" = "beat" ]; then
    poetry run celery -A celery_app beat -l info
fi
