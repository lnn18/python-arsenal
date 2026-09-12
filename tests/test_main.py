import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.integrations.coingecko_client import COINGECKO_URL
from app.integrations.trm_client import TRM_URL
from app.main import app

client = TestClient(app)

MOCK_TRM = [{"valor": "4000.0"}]
MOCK_BITCOIN = {"bitcoin": {"usd": 65000.0}}


@respx.mock
def test_home_shows_current_trm() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))
    respx.get(COINGECKO_URL).mock(return_value=Response(200, json=MOCK_BITCOIN))

    response = client.get("/")

    assert response.status_code == 200
    assert "4,000.00" in response.text


@respx.mock
def test_home_shows_bitcoin_price_in_usd_and_cop() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))
    respx.get(COINGECKO_URL).mock(return_value=Response(200, json=MOCK_BITCOIN))

    response = client.get("/")

    assert response.status_code == 200
    assert "65,000.00" in response.text
    assert "260,000,000.00" in response.text


@respx.mock
def test_convertir_returns_amount_in_cop() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))

    response = client.get("/convertir", params={"monto": 100})

    assert response.status_code == 200
    assert "400,000.00" in response.text


@respx.mock
def test_trm_json_endpoint() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))

    response = client.get("/trm")

    assert response.status_code == 200
    body = response.json()
    assert body["valor"] == 4000.0
    assert body["moneda"] == "USD/COP"


@respx.mock
def test_bitcoin_json_endpoint() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))
    respx.get(COINGECKO_URL).mock(return_value=Response(200, json=MOCK_BITCOIN))

    response = client.get("/bitcoin")

    assert response.status_code == 200
    body = response.json()
    assert body["precio_usd"] == 65000.0
    assert body["trm"] == 4000.0
    assert body["precio_cop"] == 65000.0 * 4000.0
    assert body["fuente"] == "CoinGecko"


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
