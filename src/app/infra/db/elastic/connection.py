from elasticsearch import AsyncElasticsearch, Elasticsearch

from app.settings import settings

aes = AsyncElasticsearch([settings.elastic.LIST_DSN[0]])

es = Elasticsearch([settings.elastic.LIST_DSN[0]])
