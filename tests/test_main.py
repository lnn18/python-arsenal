import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.integrations.trm_client import TRM_URL
from app.main import app

client = TestClient(app)

MOCK_TRM = [{"valor": "4000.0"}]


@respx.mock
def test_home_shows_current_trm() -> None:
    respx.get(TRM_URL).mock(return_value=Response(200, json=MOCK_TRM))

    response = client.get("/")

    assert response.status_code == 200
    assert "4,000.00" in response.text


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


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
