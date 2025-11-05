import requests
import json
import os
import re

# --- 1. CONFIGURAÇÃO DA CHAVE API ---
# (Esta é a chave que você já usou e que funcionou)
API_KEY = "AIzaSyC9HLiKBIf-8fmQmqbc5uTHbPra-jx8xV8"
# ------------------------------------

# URL da API Gemini
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

SISTEMA_PROMPT = """
Você é 'Pedro', um analista de sentimento de mercado.
Sua função é analisar notícias recentes (fornecidas pela ferramenta de busca) sobre uma ação específica.
Sua resposta DEVE conter um único bloco de código JSON (```json ... ```) e nada mais.
"""

def extract_json_from_text(text: str) -> str:
    """
    Extrai uma string JSON de dentro de um bloco de código markdown (```json ... ```)
    """
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Se não encontrar o bloco, assume que o texto *é* o JSON
    stripped_text = text.strip()
    if stripped_text.startswith('{') and stripped_text.endswith('}'):
        return stripped_text
        
    raise ValueError("Nenhum JSON válido encontrado na resposta da IA.")

def agente_pedro_analisar(ticker: str):
    """
    Executa o Agente "Pedro": analisa o sentimento da mídia sobre um ticker.
    Retorna um dicionário com a análise ou None em caso de erro.
    """
    print(f"--- Agente Pedro iniciando ---")
    print(f"Analisando sentimento de mercado para: {ticker}...")

    # A tarefa é dinâmica baseada no ticker
    tarefa_prompt = f"""
    Analise o sentimento atual do mercado (Positivo, Negativo ou Neutro) para a ação {ticker}, com base nas notícias mais recentes.
    Forneça sua análise APENAS no formato JSON com os campos "sentimento" e "resumo_analise".
    O resumo da análise deve ser em português.
    """

    payload = {
        "contents": [{"parts": [{"text": tarefa_prompt}]}],
        "systemInstruction": {"parts": [{"text": SISTEMA_PROMPT}]},
        "tools": [{"google_search": {}}],
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=60)
        response.raise_for_status() # Lança um erro para status 4xx/5xx
        data = response.json()

        # Extração do JSON
        raw_text_response = data['candidates'][0]['content']['parts'][0]['text']
        analise_json_text = extract_json_from_text(raw_text_response)
        analise_data = json.loads(analise_json_text) # Converte para dict

        # Extração das Fontes
        fontes = []
        if 'groundingMetadata' in data['candidates'][0] and 'groundingAttributions' in data['candidates'][0]['groundingMetadata']:
            fontes = [
                {"uri": attr['web']['uri'], "title": attr['web']['title']}
                for attr in data['candidates'][0]['groundingMetadata']['groundingAttributions']
            ]

        resultado_final = {
            "agente": "Pedro",
            "ticker": ticker,
            "analise": analise_data,
            "fontes": fontes
        }
        
        print("Agente 'Pedro' concluiu a análise de sentimento.")
        
        # 5. RETORNAR a análise (esta é a mudança principal)
        return resultado_final

    except requests.exceptions.HTTPError as e:
        print(f"\n--- ERRO NA CHAMADA API (Pedro) ---")
        print(f"A API retornou um erro: {e}")
        try:
            print("Resposta da API:", e.response.json())
        except json.JSONDecodeError:
            print("Resposta da API (não-JSON):", e.response.text)
        return None # Retorna None em caso de erro
    except Exception as e:
        print(f"\n--- ERRO INESPERADO (Pedro) ---")
        print(f"Ocorreu um erro: {e}")
        return None # Retorna None em caso de erro

# --- Ponto de Entrada Principal (para testar "Pedro" isoladamente) ---
if __name__ == "__main__":
    # Este bloco agora serve apenas para testar este script
    resultado = agente_pedro_analisar("PETR4.SA")
    if resultado:
        print("\n--- Teste do Pedro (Resultado) ---")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

