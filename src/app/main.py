import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.elastic.connection import es
from settings import settings
from routers.views import router

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

    if not es.indices.exists(settings.elastic.INDEX):
        es.indices.create(settings.elastic.INDEX)
        
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.uvicorn.HOST, port=settings.uvicorn.PORT, reload=True
    )
