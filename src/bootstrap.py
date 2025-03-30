from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

import firebase_admin
from aiokafka import AIOKafkaConsumer
from aiokafka.util import create_task
from fastapi import APIRouter, FastAPI
from fastapi.responses import UJSONResponse
from helpers.api.bootstrap.setup_error_handlers import setup_error_handlers
from helpers.api.middleware.auth import AuthMiddleware
from helpers.api.middleware.trace_id.middleware import TraceIdMiddleware
from helpers.api.middleware.unexpected_errors.middleware import ErrorsHandlerMiddleware
from helpers.sqlalchemy.client import SQLAlchemyClient
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import PostgresDsn

from src.kafka.emails.views import mail_listener
from src.kafka.pushes.views import pushes_listener
from src.settings import get_settings
from src.web.api.devices.views import devices_router


@lru_cache
def make_db_client(dsn: PostgresDsn = get_settings().postgres_dsn) -> SQLAlchemyClient:
    return SQLAlchemyClient(dsn=dsn)


def initialize_firebase():
    cred = firebase_admin.credentials.Certificate(get_settings().FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa
) -> AsyncGenerator[dict[str, Any], None]:
    client = make_db_client()
    initialize_firebase()
    kafka_consumer = AIOKafkaConsumer(
        *get_settings().kafka.topics,
        bootstrap_servers=get_settings().kafka.bootstrap_servers,
        group_id=get_settings().kafka.group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    await kafka_consumer.start()
    create_task(pushes_listener.listen(kafka_consumer))
    create_task(mail_listener.listen(kafka_consumer))

    try:
        yield {
            'db_client': client,
        }
    finally:
        await client.close()
        await kafka_consumer.stop()


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(ErrorsHandlerMiddleware, is_debug=get_settings().debug)  # type: ignore
    app.add_middleware(TraceIdMiddleware)  # type: ignore
    app.add_middleware(AuthMiddleware, key=get_settings().jwt_key)  # type: ignore


def setup_api_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix='/notifications/api')
    api_router.include_router(devices_router, prefix='/devices', tags=['devices'])
    app.include_router(router=api_router)


def setup_prometheus(app: FastAPI) -> None:
    Instrumentator(should_group_status_codes=False).instrument(app).expose(
        app, should_gzip=True, name='prometheus_metrics', endpoint='/metrics'
    )


def make_app() -> FastAPI:
    app = FastAPI(
        title='notifications',
        lifespan=_lifespan,
        docs_url='/notifications/api/docs',
        redoc_url='/notifications/api/redoc',
        openapi_url='/notifications/api/openapi.json',
        default_response_class=UJSONResponse,
    )

    setup_error_handlers(app, is_debug=get_settings().debug)
    setup_prometheus(app)
    setup_api_routers(app)
    setup_middlewares(app)

    return app
