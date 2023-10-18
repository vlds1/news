from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status, HTTPException
from pydantic import ValidationError
from services.elastic import ElasticCatalogService
from dependencies.dependencies import get_catalog_service

from routers.schemas import NewsCreatedSchema, HealthcheckSchema, NewsHits

router = APIRouter()


@router.get(
    "/healthcheck/",
    responses={status.HTTP_200_OK: {}},
    response_model=HealthcheckSchema,
    summary="Проверка - работает ли эластик",
)
async def healthcheck(
    catalog_service: Annotated[ElasticCatalogService, Depends(get_catalog_service)]
):
    try:
        return {"aes_available": await catalog_service.ping()}
    except Exception as err:
        return HTTPException(status_code=500, detail=str(err))


@router.get(
    "/news/",
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
    status_code=status.HTTP_200_OK,
    response_model=NewsHits,
    summary="Получение всех новостей",
)
async def get_all_news(
    catalog_service: Annotated[ElasticCatalogService, Depends(get_catalog_service)]
):
    try:
        return await catalog_service.get_all_news()
    except Exception as err:
        raise HTTPException(
            detail=err, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(
    "/news",
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
    status_code=status.HTTP_200_OK,
    response_model=NewsHits,
    summary="Поиск новостей",
)
async def find_news(
    catalog_service: Annotated[ElasticCatalogService, Depends(get_catalog_service)],
    find_str: str | None = None,
    doc_id: str | None = None,
):
    try:
        return await catalog_service.find_news(find_str, doc_id)
    except Exception as err:
        raise HTTPException(detail=err, status_code=400)


@router.post(
    "/new_news/",
    responses={
        status.HTTP_201_CREATED: {},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
    status_code=status.HTTP_201_CREATED,
    response_model=NewsCreatedSchema,
    summary="Добавление новой новости",
)
async def insert_news(
    catalog_service: Annotated[ElasticCatalogService, Depends(get_catalog_service)],
    data: NewsCreatedSchema = Body(),
):
    try:
        return catalog_service.insert_news(data)
    except ValidationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)


@router.delete(
    "/news",
    responses={
        status.HTTP_201_CREATED: {},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление новости",
)
async def delete_news(
    catalog_service: Annotated[ElasticCatalogService, Depends(get_catalog_service)],
    id: str = Query(...),
):
    try:
        await catalog_service.delete_news(id=id)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
