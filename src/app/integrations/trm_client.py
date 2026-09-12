"""Integración con la TRM oficial (Superintendencia Financiera de Colombia, vía datos.gov.co)."""

from app.http_client import get_json

TRM_URL = "https://www.datos.gov.co/resource/mcec-87by.json"


async def get_trm() -> float:
    """Devuelve la TRM (tasa de cambio USD/COP) vigente más reciente."""
    data = await get_json(TRM_URL, params={"$limit": "1"})
    return float(data[0]["valor"])
