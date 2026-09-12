"""Integración con la API pública de CoinGecko."""

from app.http_client import get_json

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


async def get_bitcoin_price_usd() -> float:
    """Devuelve el precio actual de Bitcoin en USD."""
    data = await get_json(COINGECKO_URL, params={"ids": "bitcoin", "vs_currencies": "usd"})
    return float(data["bitcoin"]["usd"])
