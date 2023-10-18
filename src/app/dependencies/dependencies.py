from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.elastic import ElasticCatalogService

from settings import settings


async def elastic_search_connection() -> AsyncElasticsearch:
    return AsyncElasticsearch([settings.elastic.LIST_DSN[0]])


async def get_catalog_service(
    aes: Annotated[AsyncElasticsearch, Depends(elastic_search_connection)]
) -> ElasticCatalogService:
    return ElasticCatalogService(aes=aes, index=settings.elastic.INDEX)
