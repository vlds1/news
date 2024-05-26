from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rest.controllers import router
from app.infra.db.elastic.connection import es
from app.settings import settings
from app.utils import init_es


@asynccontextmanager
async def app_lifespan():
    "Пока не нужна"


def create_app():
    app = FastAPI()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    init_es()
    if not es.indices.exists(settings.elastic.INDEX):
        es.indices.create(settings.elastic.INDEX)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.uvicorn.HOST, port=settings.uvicorn.PORT, reload=True
    )
