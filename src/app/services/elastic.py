from elasticsearch import AsyncElasticsearch
from routers.schemas import NewsFullSchema
from settings import settings


class ElasticCatalogService:
    def __init__(self, aes: AsyncElasticsearch, index: str) -> None:
        self.aes = aes
        self.index = index

    async def get_all_news(self) -> dict:
        query: dict[str, object] = {"match_all": {}}
        all_news = await self.aes.search(index=settings.elastic.INDEX, query=query)
        return all_news

    async def find_news(self, find_str: str, doc_id: str):
        if doc_id:
            query = {"terms": {"_id": [doc_id]}}
        if find_str:
            query = {
                "query_string": {
                    "query": f"*{doc_id if doc_id is not None else find_str}*"
                }
            }
        return await self.aes.search(index=settings.elastic.INDEX, query=query)

    async def insert_news(self, data: NewsFullSchema):
        data = await self.aes.index(index=settings.elastic.INDEX, document=data.dict())

    async def delete_news(self, id: str):
        await self.aes.delete(id=id, index=settings.elastic.INDEX)

    async def ping(self):
        return await self.aes.ping()
