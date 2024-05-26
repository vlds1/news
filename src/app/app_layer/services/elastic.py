from app.api.rest.schemas import NewsFullSchema
from app.infra.repositories.elastic import ElasticRepository


class ElasticService:
    def __init__(self, repo: ElasticRepository) -> None:
        self.repo: ElasticRepository = repo

    async def get_all_news(self) -> dict:
        return await self.repo.get_all_news()

    async def find_news(self, find_str: str, doc_id: str):
        return await self.repo.find_news(find_str, doc_id)

    async def insert_news(self, data: NewsFullSchema):
        data = await self.repo.insert_news(data)

    async def delete_news(self, id: str):
        await self.repo.delete_news(id)

    async def ping(self):
        return await self.repo.ping()
