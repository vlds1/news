from app.infra.db.elastic.connection import es
from app.settings import settings


def init_es():
    if es.indices.exists(index=settings.elastic.INDEX):
        return

    es.indices.create(index=settings.elastic.INDEX)

    return
