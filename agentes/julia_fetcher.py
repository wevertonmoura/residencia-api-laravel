import yfinance as yf
import logging
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_fixed
from models import StockData # Importa do nosso novo arquivo

logger = logging.getLogger("AgenteJulia")

class YahooFinanceProvider:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_ticker_data(self, ticker: str) -> Optional[StockData]:
        try:
            logger.info(f"Conectando ao Yahoo Finance para: {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or 'currentPrice' not in info:
                logger.warning(f"Dados incompletos para {ticker}")
                return None
            
            # Cálculo Técnico
            historico = stock.history(period="200d")
            sma_200 = historico['Close'].mean() if not historico.empty else 0.0
            preco_atual = info.get("currentPrice", 0.0)
            
            tendencia = "ALTA" if preco_atual > sma_200 else "BAIXA"

            # Retorna o modelo Pydantic validado
            return StockData(
                ticker=ticker.upper(),
                price=preco_atual,
                open_price=info.get("open", 0.0),
                volume=info.get("volume", 0),
                market_cap=info.get("marketCap", 0),
                high_52w=info.get("fiftyTwoWeekHigh", 0.0),
                low_52w=info.get("fiftyTwoWeekLow", 0.0),
                summary=info.get("longBusinessSummary", "N/A"),
                media_movel_200=round(sma_200, 2),
                tendencia_longo_prazo=tendencia
            )
        except Exception as e:
            logger.error(f"Erro no Yahoo Finance ({ticker}): {e}")
            raise e # O @retry vai pegar isso e tentar de novo

class JuliaAgent:
    def __init__(self, provider: YahooFinanceProvider):
        self.provider = provider

    def execute(self, ticker: str) -> Optional[StockData]:
        return self.provider.fetch_ticker_data(ticker)