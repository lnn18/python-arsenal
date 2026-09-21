"""Modelos Pydantic — contratos de request/response de la app."""

from pydantic import BaseModel


class TrmResponse(BaseModel):
    moneda: str
    valor: float
    fuente: str


class BitcoinResponse(BaseModel):
    precio_usd: float
    precio_cop: float
    trm: float
    fuente: str


class HealthResponse(BaseModel):
    status: str
