from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.db import MongoDB
from endpoints.users import router as users_router
from endpoints.foods import router as foods_router
from endpoints.restaurants import router as restaurants_router
from endpoints.tables import router as tables_router
from custom_logging.middleware import LoggingMiddleware
import logging


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

app.include_router(users_router)
app.include_router(foods_router)
app.include_router(restaurants_router)
app.include_router(tables_router)
app.add_middleware(LoggingMiddleware)
