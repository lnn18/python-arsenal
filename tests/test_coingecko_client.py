import httpx
import pytest
import respx
from httpx import Response

from app.integrations.coingecko_client import COINGECKO_URL, get_bitcoin_price_usd

SAMPLE_RESPONSE = {"bitcoin": {"usd": 65000.0}}


@pytest.mark.asyncio
@respx.mock
async def test_get_bitcoin_price_usd_returns_current_value() -> None:
    respx.get(COINGECKO_URL).mock(return_value=Response(200, json=SAMPLE_RESPONSE))

    result = await get_bitcoin_price_usd()

    assert result == 65000.0


@pytest.mark.asyncio
@respx.mock
async def test_get_bitcoin_price_usd_propagates_http_errors() -> None:
    respx.get(COINGECKO_URL).mock(return_value=Response(503))

    with pytest.raises(httpx.HTTPStatusError):
        await get_bitcoin_price_usd()
