from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.db import MongoDB
from endpoints.foods import router as foods_router
from endpoints.restaurants import router as restaurants_router
from endpoints.tables import router as tables_router
from endpoints.auth import router as auth_router
from custom_logging.middleware import LoggingMiddleware
import logging
from conf import ALLOWED_HOSTS

from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await MongoDB.connect()
        yield
    except Exception as e:
        logger = logging.getLogger('error')
        logger.error(f"Error during startup: {e}")
    finally:
        await MongoDB.close()

app = FastAPI(lifespan=lifespan)

app.include_router(foods_router)
app.include_router(restaurants_router)
app.include_router(tables_router)
app.include_router(auth_router)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
