from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- IMPORTANTE PARA O FRONTEND
import threading
import logging
import os
from dotenv import load_dotenv

# Importações dos Agentes
from julia_fetcher import YahooFinanceProvider, JuliaAgent
from pedro_analyzer import GeminiProvider, PedroAgent
from key_writer import GeminiWriter, APILaravelPublisher, KeyAgent

load_dotenv()
app = Flask(__name__)

# --- CONFIGURAÇÃO SÊNIOR DE CORS ---
# Permite que qualquer origem acesse a API (em produção, restrinja ao seu domínio)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("API_Manager")

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
LARAVEL_URL = os.getenv("LARAVEL_API_URL")

def worker_analise(tickers):
    """Worker que processa a lista de ações em background"""
    if not GEMINI_KEY:
        logger.error("Sem chave API!")
        return

    julia = JuliaAgent(YahooFinanceProvider())
    # Usando o provider simplificado (sem google search) para evitar erros
    pedro = PedroAgent(GeminiProvider(GEMINI_KEY))
    key = KeyAgent(GeminiWriter(GEMINI_KEY), APILaravelPublisher(LARAVEL_URL))

    for ticker in tickers:
        logger.info(f"--- Processando {ticker} ---")
        try:
            dados_julia = julia.execute(ticker)
            if not dados_julia: continue

            dados_pedro = pedro.execute(ticker)
            # O Pedro agora sempre retorna algo (com ou sem busca), então validamos o objeto
            if not dados_pedro: continue

            key.processar_e_publicar(ticker, dados_julia, dados_pedro)
        except Exception as e:
            logger.error(f"Erro no ciclo de {ticker}: {e}")

@app.route('/gerar', methods=['POST'])
def gerar():
    """Endpoint chamado pelo Painel HTML"""
    data = request.json
    scope = data.get('scope', 'all')
    ticker_single = data.get('ticker')

    # Lógica de seleção
    tickers = ["PETR4.SA", "MGLU3.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]
    if scope == 'single' and ticker_single:
        tickers = [ticker_single]

    # Inicia thread para não travar o painel
    threading.Thread(target=worker_analise, args=(tickers,)).start()
    
    return jsonify({
        "status": "success", 
        "message": "Agentes iniciados!", 
        "targets": tickers
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)