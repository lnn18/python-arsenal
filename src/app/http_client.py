"""Cliente HTTP compartido con retry/backoff para integraciones con APIs externas."""

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

DEFAULT_TIMEOUT = 5.0


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, max=4),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
)
async def get_json(url: str, *, params: dict[str, Any] | None = None) -> Any:
    """Hace GET a una URL y devuelve el JSON parseado, reintentando ante errores de red."""
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
