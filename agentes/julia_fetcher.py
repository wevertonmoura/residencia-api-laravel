import yfinance as yf
import logging
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger("AgenteJulia")

# --- Entidade Atualizada (Com dados técnicos) ---
@dataclass
class StockData:
    ticker: str
    price: float
    open_price: float
    volume: int
    market_cap: int
    high_52w: float
    low_52w: float
    summary: str
    # NOVOS CAMPOS TÉCNICOS
    media_movel_200: float
    tendencia_longo_prazo: str 

class FinancialDataProvider(ABC):
    @abstractmethod
    def fetch_ticker_data(self, ticker: str) -> Optional[StockData]:
        pass

class YahooFinanceProvider(FinancialDataProvider):
    def fetch_ticker_data(self, ticker: str) -> Optional[StockData]:
        try:
            logger.info(f"Conectando ao Yahoo Finance para: {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or 'currentPrice' not in info:
                logger.warning(f"Dados incompletos recebidos para {ticker}")
                return None
            
            # --- CÁLCULO DE INTELIGÊNCIA DE DADOS ---
            # Pegamos o histórico de 200 dias
            historico = stock.history(period="200d")
            
            sma_200 = 0.0
            tendencia = "Indefinida"

            if not historico.empty:
                sma_200 = historico['Close'].mean()
                preco_atual = info.get("currentPrice", 0.0)
                
                # Define a tendência
                if preco_atual > sma_200:
                    tendencia = "ALTA (Preço acima da média de 200 dias)"
                else:
                    tendencia = "BAIXA (Preço abaixo da média de 200 dias)"
            # ----------------------------------------

            return StockData(
                ticker=ticker,
                price=info.get("currentPrice", 0.0),
                open_price=info.get("open", 0.0),
                volume=info.get("volume", 0),
                market_cap=info.get("marketCap", 0),
                high_52w=info.get("fiftyTwoWeekHigh", 0.0),
                low_52w=info.get("fiftyTwoWeekLow", 0.0),
                summary=info.get("longBusinessSummary", "N/A"),
                # Passamos os novos dados calculados
                media_movel_200=round(sma_200, 2),
                tendencia_longo_prazo=tendencia
            )
        except Exception as e:
            logger.error(f"Erro ao buscar dados no Yahoo Finance: {e}")
            return None

class JuliaAgent:
    def __init__(self, provider: FinancialDataProvider):
        self.provider = provider

    def execute(self, ticker: str) -> Optional[Dict[str, Any]]:
        logger.info("--- Agente Júlia Iniciando ---")
        stock_data = self.provider.fetch_ticker_data(ticker)
        
        if not stock_data:
            return None
        
        return {
            "titulo_base": f"Análise Técnica e Fundamentalista: {stock_data.ticker}",
            "dados_financeiros": asdict(stock_data), # Converte tudo para dict automaticamente
            "ticker": stock_data.ticker,
            "status": "success"
        }