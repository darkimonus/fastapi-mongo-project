import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from custom_logging.config import format_headers
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()
        body = await request.body()
        logger.info(f"Incoming Request - {request.method} {request.url}")
        logger.info(f"Headers:\n{format_headers(dict(request.headers))}")
        if body:
            logger.info(f"Body: {body.decode('utf-8')}")

        response = await call_next(request)

        process_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response - Status Code: {response.status_code}")
        logger.info(f"Processing Time: {process_time:.2f}s" + "\n" + "-" * 80 + "\n")

        return response

    @staticmethod
    async def _async_iter(content):
        """
        Генерирует асинхронный итератор для переданного контента.
        """
        yield content
