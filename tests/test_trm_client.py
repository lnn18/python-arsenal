import httpx
import pytest
import respx
from httpx import Response

from app.integrations.trm_client import TRM_URL, get_trm

SAMPLE_RESPONSE = [
    {
        "valor": "3101.0",
        "unidad": "COP",
        "vigenciadesde": "2026-09-11T00:00:00.000",
        "vigenciahasta": "2026-09-11T00:00:00.000",
    }
]


@pytest.mark.asyncio
@respx.mock
async def test_get_trm_returns_current_value() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=SAMPLE_RESPONSE))

    result = await get_trm()

    assert result == 3101.0


@pytest.mark.asyncio
@respx.mock
async def test_get_trm_propagates_http_errors() -> None:
    respx.get(TRM_URL).mock(return_value=Response(503))

    with pytest.raises(httpx.HTTPStatusError):
        await get_trm()
