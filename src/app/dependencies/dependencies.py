from services.elastic import ElasticCatalogService
from app.db.elastic.connection import aes
from settings import settings


async def get_catalog_service() -> ElasticCatalogService:
    return ElasticCatalogService(aes=aes, index=settings.elastic.INDEX)
