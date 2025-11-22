from flask import Flask, request, jsonify
import threading
import logging
from dotenv import load_dotenv
import os

# Importa seus agentes
from julia_fetcher import YahooFinanceProvider, JuliaAgent
from pedro_analyzer import GeminiProvider, PedroAgent
from key_writer import GeminiWriter, APILaravelPublisher, KeyAgent

# Configuração
load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API_Python")

# Carteira Padrão
CARTEIRA_PADRAO = ["PETR4.SA", "MGLU3.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]

def executar_analise(tickers):
    """Função que roda em segundo plano para não travar o servidor"""
    gemini_key = os.getenv("GEMINI_API_KEY")
    laravel_url = os.getenv("LARAVEL_API_URL")
    
    provider_julia = YahooFinanceProvider()
    julia = JuliaAgent(provider_julia)
    
    provider_pedro = GeminiProvider(api_key=gemini_key, model="gemini-2.5-flash-preview-09-2025")
    pedro = PedroAgent(provider=provider_pedro)
    
    writer = GeminiWriter(api_key=gemini_key)
    publisher = APILaravelPublisher(api_url=laravel_url)
    key = KeyAgent(writer=writer, publisher=publisher)

    logger.info(f"🚀 Iniciando análise para: {tickers}")

    for ticker in tickers:
        logger.info(f"Analisando {ticker}...")
        dados_julia = julia.execute(ticker)
        if not dados_julia: continue
            
        dados_pedro = pedro.execute(ticker)
        if not dados_pedro: continue
            
        key.processar_e_publicar(ticker, dados_julia, dados_pedro)
    
    logger.info("✅ Ciclo finalizado via API!")

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "agentes": ["Julia", "Pedro", "Key"]})

@app.route('/gerar', methods=['POST'])
def gerar_conteudo():
    """Recebe { 'tickers': ['PETR4.SA'] } ou { 'tickers': 'all' }"""
    data = request.json
    alvos = data.get('tickers', 'all')
    
    lista_final = []
    if alvos == 'all':
        lista_final = CARTEIRA_PADRAO
    elif isinstance(alvos, list):
        lista_final = alvos
    else:
        return jsonify({"error": "Formato inválido"}), 400

    # Roda em Thread separada para responder o Laravel rápido
    thread = threading.Thread(target=executar_analise, args=(lista_final,))
    thread.start()

    return jsonify({"message": "Processamento iniciado", "targets": lista_final}), 202

if __name__ == "__main__":
    # Roda na porta 5000 e aceita conexões de fora do container (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)