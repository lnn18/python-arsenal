# Cambio Hoy

Conversor USD → COP usando la TRM oficial (Superintendencia Financiera de Colombia, vía [datos.gov.co](https://www.datos.gov.co/)).

## Estructura

```
src/app/
├── main.py                  # FastAPI: home (HTML), /convertir, /trm, /health
├── schemas.py                # Contratos Pydantic de request/response
├── http_client.py            # Cliente HTTP compartido con retry/backoff (httpx + tenacity)
└── integrations/
    ├── trm_client.py         # Integración con la TRM oficial
    └── coingecko_client.py   # Integración con CoinGecko (precio de Bitcoin)
```

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync --all-extras
```

## Uso

```bash
make dev          # servidor con reload en http://127.0.0.1:8000
make test          # pytest
make lint          # ruff check
make typecheck     # mypy
make check         # lint + typecheck + test
```

## Endpoints

- `GET /` — página HTML con el conversor y el precio de Bitcoin
- `GET /convertir?monto=100` — convierte USD a COP (HTML)
- `GET /trm` — TRM vigente (JSON)
- `GET /bitcoin` — precio de Bitcoin en USD y COP, vía CoinGecko (JSON)
- `GET /health` — health check
