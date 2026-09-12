# Cambio Hoy

FastAPI que expone indicadores financieros reales (TRM, precios de mercado, etc.) obtenidos
de APIs públicas externas. El valor del proyecto depende de que esas integraciones sean
correctas, resilientes y verificables — no de la cantidad de endpoints.

## Stack (no usar alternativas legacy)

- Gestor de paquetes y entornos: **uv** (`uv sync`, `uv run`) — nunca `pip install` suelto ni `requirements.txt`.
- HTTP: **httpx** async — nunca `requests` (no soporta async) ni `urllib`.
- Retry/backoff: **tenacity** — nunca loops manuales de `time.sleep` + reintento.
- Validación/contratos: **Pydantic v2** (`BaseModel`) — nunca dicts sueltos ni `dataclasses` para I/O externo.
- Lint + formato: **ruff** (`ruff check`, `ruff format`) — nunca `flake8`/`black`/`isort` por separado.
- Tipado: **mypy --strict** — todo el código en `src/app` debe tipar limpio en modo estricto.
- Tests: **pytest** + **pytest-asyncio** (modo auto) + **respx** para mockear HTTP — nunca `unittest.mock` para HTTP ni llamadas reales a APIs externas en tests.

Comandos: `make dev`, `make test`, `make lint`, `make typecheck`, `make check` (lint+typecheck+test).

## Cómo se construye una integración nueva

Cada integración a una API externa sigue el mismo patrón, sin excepciones. Mirar
`src/app/integrations/trm_client.py` como referencia canónica.

1. **Cliente** en `src/app/integrations/<servicio>_client.py`:
   - Una función async pública por dato expuesto (ej. `get_trm() -> float`), con docstring de una línea.
   - La URL base va en una constante a nivel de módulo en mayúsculas (ej. `TRM_URL`), nunca hardcodeada dentro de la función — los tests la importan para mockear con `respx.get(URL)`.
   - Todas las llamadas HTTP pasan por `app.http_client.get_json` (retry + timeout compartidos). No crear clientes `httpx` sueltos dentro de una integración.
   - La función retorna tipos primitivos o un modelo Pydantic ya parseado — nunca el JSON crudo.
   - No capturar excepciones de red aquí: dejar que `httpx.HTTPError` se propague. El manejo de errores de cara al usuario vive en `main.py`.

2. **Schema** en `src/app/schemas.py`:
   - Un `BaseModel` de respuesta por endpoint JSON nuevo, con nombres de campo en español consistentes con los modelos existentes (`valor`, `fuente`, `moneda`, etc.).

3. **Endpoint** en `src/app/main.py`:
   - Todo endpoint que dependa de una integración externa debe envolver la llamada en `try/except httpx.HTTPError` y responder `HTTPException(status_code=502, ...)` — nunca dejar que un error de red externo se convierta en un 500 genérico.
   - Endpoints HTML (`response_class=HTMLResponse`) degradan con un mensaje legible cuando la fuente falla; nunca deben romper la carga de toda la página porque una sola integración falló (ver `home()`: si una fuente falla, esa sección muestra un mensaje, el resto de la página se sigue renderizando).
   - Endpoints JSON usan `response_model=<Schema>` para que el contrato quede validado y documentado en `/docs` automáticamente.

4. **Tests**, dos archivos obligatorios por integración nueva:
   - `tests/test_<servicio>_client.py`: al menos un caso feliz (`respx.mock` devolviendo un payload de ejemplo) y un caso de error HTTP (`respx` devuelve 5xx, se espera que la excepción se propague).
   - Casos nuevos o modificados en `tests/test_main.py`: mockear con `respx` la integración vía su constante `_URL` importada, nunca golpear la red real. Verificar tanto el degradado ante fallo como el resultado exitoso.
   - Nunca marcar un test como skip para "arreglarlo después" — si una integración no se puede testear determinísticamente con `respx`, el diseño del cliente está mal.

## Reglas de seguridad y calidad no negociables

- Nunca loguear ni exponer API keys, tokens o URLs con credenciales embebidas en respuestas o commits.
- Todo output que interpole datos externos en HTML (f-strings en `main.py`) debe tratarse como no confiable: no se ejecuta código de usuario aquí, pero no agregar interpolación de texto libre de una API externa sin escapar si en el futuro se agregan campos de texto (hoy solo se interpolan números formateados, mantenerlo así o escapar explícitamente).
- `ruff` corre con las reglas `S` (bandit/seguridad) activas — no silenciar un hallazgo `S` con `# noqa` sin justificarlo en el mismo comentario.
- Antes de considerar terminada una integración: `make check` debe pasar limpio. No se hacen commits con lint, tipos o tests rotos.
