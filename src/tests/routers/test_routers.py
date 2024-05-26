import pytest

from app.settings import settings

pytestmark = [pytest.mark.asyncio]


@pytest.fixture()
async def aes_index():
    return f"{settings.elastic.INDEX}_test"


async def test_healthcheck(client):
    response = await client.get("/healthcheck/")
    assert response == True
