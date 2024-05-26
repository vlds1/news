from asyncio import AbstractEventLoop
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from httpx import AsyncClient

from app.api.main import app

# from app.settings import settings


list_dns = f"http://elastic:changeme@localhost:9200/"


@asynccontextmanager
async def aes_client(eas_list_dns=list_dns):
    aes = AsyncElasticsearch([eas_list_dns])
    yield aes
    await aes.close()


@pytest.fixture()
async def get_aes_client() -> AsyncElasticsearch:
    async with aes_client() as client:
        return await client


@pytest.fixture()
async def fastapi_app(app=app) -> FastAPI:
    return app


@pytest.fixture()
async def client(fastapi_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app) as client:
        yield client
