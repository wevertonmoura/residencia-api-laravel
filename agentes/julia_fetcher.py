import yfinance as yf
import json
import requests # O "Key" vai importar o 'requests' e a URL daqui

# --- Configuração ---
# URL da sua API Laravel (o "Key" vai usar isto)
LARAVEL_API_URL = "http://localhost/api/artigos"

def agente_julia_buscar_dados(ticker: str):
    """
    Executa o Agente "Júlia": busca dados financeiros de um ticker.
    """
    print(f"--- Agente Júlia iniciando ---")
    print(f"Buscando dados para: {ticker}...")
    
    try:
        # 1. Conectar ao Yahoo Finance
        acao = yf.Ticker(ticker)
        
        # 2. Obter informações da ação
        info = acao.info

        # 3. Filtrar os dados que queremos (conforme a proposta)
        dados_filtrados = {
            "Preço Atual": info.get("currentPrice"),
            "Abertura": info.get("open"),
            "Volume": info.get("volume"),
            "Valor de Mercado": info.get("marketCap"),
            "Máxima 52 Semanas": info.get("fiftyTwoWeekHigh"),
            "Mínima 52 Semanas": info.get("fiftyTwoWeekLow"),
            "Resumo do Negócio": info.get("longBusinessSummary", "N/A"),
        }
        
        print("Dados coletados com sucesso do Yahoo Finance.")
        
        # 4. Preparar os dados para o Agente "Key"
        dados_para_key = {
            "titulo_base": f"Análise de Dados Brutos: {ticker}",
            "dados_financeiros": json.dumps(dados_filtrados, indent=2, ensure_ascii=False),
            "ticker": ticker,
        }
        
        # 5. RETORNAR os dados (esta é a mudança principal)
        return dados_para_key

    except Exception as e:
        print(f"\n--- ERRO (Júlia) ---")
        print(f"Não foi possível buscar dados do Yahoo Finance para {ticker}.")
        print(f"Detalhes: {e}")
        return None # Retorna None em caso de erro

# --- Ponto de Entrada Principal (para testar "Júlia" isoladamente) ---
if __name__ == "__main__":
    # Este bloco agora serve apenas para testar este script
    dados = agente_julia_buscar_dados("PETR4.SA")
    if dados:
        print("\n--- Teste da Júlia (Resultado) ---")
        print(json.dumps(dados, indent=2, ensure_ascii=False))

