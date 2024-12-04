#!/bin/bash
set -e
if [ "$CONTAINER_TYPE" = "master" ]; then
    if [ "$DEPLOYMENT_SERVER" = "False" ]; then
    poetry run uvicorn main:app --host 0.0.0.0 --port 8000
    fi
fi
