from pydantic import BaseModel, Field
from typing import List, Optional

# --- Modelos de Dados (Pydantic) ---

class StockData(BaseModel):
    ticker: str
    price: float
    open_price: float = 0.0
    volume: int = 0
    market_cap: int = 0
    high_52w: float = 0.0
    low_52w: float = 0.0
    summary: str = "N/A"
    media_movel_200: float = 0.0
    tendencia_longo_prazo: str = "Indefinida"

class FonteInfo(BaseModel):
    titulo: str
    uri: str

class AnaliseSentimento(BaseModel):
    ticker: str
    sentimento: str = Field(description="Positivo, Negativo ou Neutro")
    resumo: str
    fontes: List[FonteInfo] = []

class ArtigoFinal(BaseModel):
    titulo: str
    conteudo: str
    recomendacao: str
    ticker: str
    status: str = "rascunho"