import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.integrations.coingecko_client import get_bitcoin_price_usd
from app.integrations.trm_client import get_trm
from app.schemas import BitcoinResponse, HealthResponse, TrmResponse

app = FastAPI(title="Cambio Hoy")

PAGE_STYLE = """
<style>
  body {
    font-family: system-ui, sans-serif;
    max-width: 480px;
    margin: 4rem auto;
    padding: 0 1rem;
    color: #16324F;
  }
  h1 { font-size: 1.5rem; }
  .valor { font-size: 2.5rem; font-weight: bold; color: #16324F; margin: 0.25rem 0; }
  .fuente { color: #5B7186; font-size: 0.85rem; }
  form { margin-top: 2rem; display: flex; gap: 0.5rem; }
  input, button { padding: 0.6rem; font-size: 1rem; }
  input { flex: 1; border: 1px solid #ccc; border-radius: 4px; }
  button { background: #16324F; color: white; border: none; border-radius: 4px; cursor: pointer; }
  .resultado { margin-top: 1.5rem; padding: 1rem; background: #EAF1FB; border-radius: 8px; }
  a { color: #16324F; }
</style>
"""


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    try:
        trm = await get_trm()
        trm_html = f'<p class="valor">${trm:,.2f} COP</p>'
    except httpx.HTTPError:
        trm = None
        trm_html = "<p>No se pudo consultar la TRM en este momento.</p>"

    bitcoin_html = "<p>No se pudo consultar el precio de Bitcoin en este momento.</p>"
    if trm is not None:
        try:
            btc_usd = await get_bitcoin_price_usd()
            btc_cop = btc_usd * trm
            bitcoin_html = f"""
            <p class="valor">${btc_usd:,.2f} USD</p>
            <p class="valor">${btc_cop:,.2f} COP</p>
            <p class="fuente">Precio vía CoinGecko, convertido con la TRM oficial</p>
            """
        except httpx.HTTPError:
            pass

    return f"""
    <html><head><title>Cambio Hoy</title>{PAGE_STYLE}</head>
    <body>
      <h1>Cambio Hoy</h1>
      <p>TRM oficial (Superintendencia Financiera de Colombia):</p>
      {trm_html}
      <form action="/convertir" method="get">
        <input type="number" step="0.01" name="monto" placeholder="Monto en USD" required>
        <button type="submit">Convertir a COP</button>
      </form>
      <h1>Bitcoin</h1>
      <p>Precio actual de Bitcoin:</p>
      {bitcoin_html}
    </body></html>
    """


@app.get("/convertir", response_class=HTMLResponse)
async def convertir(monto: float = Query(..., gt=0)) -> str:
    try:
        trm = await get_trm()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="TRM provider unavailable") from exc

    total = monto * trm
    return f"""
    <html><head><title>Cambio Hoy</title>{PAGE_STYLE}</head>
    <body>
      <h1>Cambio Hoy</h1>
      <div class="resultado">
        <p>US$ {monto:,.2f} son hoy:</p>
        <p class="valor">${total:,.2f} COP</p>
        <p class="fuente">TRM: ${trm:,.2f} — Superintendencia Financiera de Colombia</p>
      </div>
      <p><a href="/">&larr; Volver</a></p>
    </body></html>
    """


@app.get("/trm", response_model=TrmResponse)
async def trm_json() -> TrmResponse:
    try:
        valor = await get_trm()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="TRM provider unavailable") from exc
    return TrmResponse(
        moneda="USD/COP",
        valor=valor,
        fuente="Superintendencia Financiera de Colombia",
    )


@app.get("/bitcoin", response_model=BitcoinResponse)
async def bitcoin_json() -> BitcoinResponse:
    try:
        trm = await get_trm()
        precio_usd = await get_bitcoin_price_usd()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Bitcoin price provider unavailable") from exc
    return BitcoinResponse(
        precio_usd=precio_usd,
        precio_cop=precio_usd * trm,
        trm=trm,
        fuente="CoinGecko",
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
