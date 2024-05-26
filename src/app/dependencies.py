from fastapi import Depends

from app.app_layer.services.elastic import ElasticService
from app.infra.db.elastic.connection import aes
from app.infra.repositories.elastic import ElasticRepository
from app.settings import settings


def get_elastic_repo() -> ElasticRepository:
    return ElasticRepository(aes=aes, index=settings.elastic.INDEX)


def get_catalog_service(
    repo: ElasticRepository = Depends(get_elastic_repo),
) -> ElasticService:
    return ElasticService(repo)
