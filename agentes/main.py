import logging
import os
import time # Import para dar uma pausa entre as requisições
from dotenv import load_dotenv

# Imports dos Agentes
try:
    from julia_fetcher import YahooFinanceProvider, JuliaAgent
    from pedro_analyzer import GeminiProvider, PedroAgent
    from key_writer import GeminiWriter, APILaravelPublisher, KeyAgent
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Orquestrador")

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"

# --- LISTA DE AÇÕES PARA O ROBÔ ---
CARTEIRA = ["PETR4.SA", "MGLU3.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]

def main():
    logger.info("=== 🚀 INICIANDO VARREDURA DA CARTEIRA ===")

    if not GEMINI_KEY or not LARAVEL_API_URL:
        logger.error("❌ Verifique suas chaves no arquivo .env")
        return

    # Inicia os Agentes (Instancia apenas uma vez para economizar memória)
    provider_julia = YahooFinanceProvider()
    julia = JuliaAgent(provider_julia)

    provider_pedro = GeminiProvider(api_key=GEMINI_KEY, model=GEMINI_MODEL)
    pedro = PedroAgent(provider=provider_pedro)

    writer_ia = GeminiWriter(api_key=GEMINI_KEY)
    publisher_laravel = APILaravelPublisher(api_url=LARAVEL_API_URL)
    key = KeyAgent(writer=writer_ia, publisher=publisher_laravel)

    # --- O LOOP MÁGICO ---
    for ticker in CARTEIRA:
        logger.info(f"\n🔄 --- Iniciando análise para: {ticker} ---")
        
        # 1. JÚLIA
        dados_julia = julia.execute(ticker)
        if not dados_julia:
            logger.warning(f"Pulo {ticker} por falha na Júlia.")
            continue # Vai para a próxima ação

        # 2. PEDRO
        dados_pedro = pedro.execute(ticker)
        if not dados_pedro:
            logger.warning(f"Pulo {ticker} por falha no Pedro.")
            continue

        # 3. KEY
        key.processar_e_publicar(ticker, dados_julia, dados_pedro)
        
        logger.info(f"✅ {ticker} finalizado com sucesso!")
        
        # Pausa de 5 segundos para não sobrecarregar a API (Rate Limit)
        time.sleep(5) 

    logger.info("\n=== 🏁 VARREDURA COMPLETA FINALIZADA ===")

if __name__ == "__main__":
    main()