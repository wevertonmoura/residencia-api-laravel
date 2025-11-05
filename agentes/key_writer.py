import requests
import json
import os
import re

# Importa as funções dos outros agentes
# Presume que este ficheiro está na MESMA pasta (agentes/) que os outros
from julia_fetcher import agente_julia_buscar_dados, LARAVEL_API_URL
from pedro_analyzer import agente_pedro_analisar, API_KEY, GEMINI_API_URL

# --- Configuração do Agente "Key" ---
TICKER_PARA_ANALISAR = "PETR4.SA" # A ação que queremos analisar

# O "prompt" (instrução) para a IA assumir a persona do "Key"
SISTEMA_PROMPT_KEY = """
Você é 'Key', um jornalista financeiro experiente e redator de artigos de investimento.
Sua função é pegar os dados brutos (de "Júlia") e uma análise de sentimento (de "Pedro") e escrever um artigo final.

O artigo deve ter:
1. Um título chamativo e profissional (máximo 100 caracteres).
2. O artigo em si (mínimo de 3 parágrafos), explicando os dados brutos e o sentimento da mídia.
3. Uma recomendação clara: "Comprar", "Vender" ou "Manter".

Sua resposta deve ser APENAS um JSON com os campos: "titulo", "conteudo" e "recomendacao".
"""

def agente_key_escrever(ticker: str, dados_julia: dict, dados_pedro: dict):
    """
    Executa o Agente "Key": Redige o artigo final com base nos dados dos outros agentes.
    """
    print(f"--- Agente Key iniciando ---")
    print(f"Redigindo artigo para: {ticker}...")
    
    # 1. Montar a tarefa para o "Key"
    # Converte os dados recebidos em strings para a IA ler
    # (Usamos .get() para segurança, caso o "Pedro" falhe em retornar a 'analise')
    string_dados_julia = json.dumps(dados_julia, indent=2, ensure_ascii=False)
    string_dados_pedro = json.dumps(dados_pedro.get('analise', {}), indent=2, ensure_ascii=False)
    
    tarefa_prompt = f"""
    Com base nos dados e na análise de sentimento abaixo, redija o artigo financeiro final.

    ### DADOS BRUTOS (Agente Júlia):
    {string_dados_julia}

    ### ANÁLISE DE SENTIMENTO (Agente Pedro):
    {string_dados_pedro}

    Por favor, redija o artigo financeiro final no formato JSON solicitado (titulo, conteudo, recomendacao).
    O artigo deve ser escrito em português do Brasil.
    """
    
    # 2. Payload para a API Gemini
    payload = {
        "contents": [{"parts": [{"text": tarefa_prompt}]}],
        "systemInstruction": {"parts": [{"text": SISTEMA_PROMPT_KEY}]},
        # 3. Configuração de Geração: Força a resposta a ser um JSON
        # (Podemos usar isto agora porque NÃO estamos a usar "tools" como o "Pedro")
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "titulo": {"type": "STRING"},
                    "conteudo": {"type": "STRING"},
                    "recomendacao": {"type": "STRING"}
                },
                "required": ["titulo", "conteudo", "recomendacao"]
            }
        }
    }
    
    try:
        # 4. Chamar a API Gemini (sem "tools")
        response = requests.post(GEMINI_API_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=120) # 2 minutos de timeout
        response.raise_for_status()
        data = response.json()
        
        # 5. Extrair o artigo JSON gerado
        # A resposta da IA (com schema JSON) está diretamente no 'text'
        artigo_json_text = data['candidates'][0]['content']['parts'][0]['text']
        artigo_data = json.loads(artigo_json_text) # dict com titulo, conteudo, recomendacao
        
        print("Agente 'Key' redigiu o artigo com sucesso.")
        return artigo_data

    except requests.exceptions.HTTPError as e:
        print(f"\n--- ERRO NA CHAMADA API (Key) ---")
        print(f"A API retornou um erro: {e}")
        try:
            print("Resposta da API:", e.response.json())
        except json.JSONDecodeError:
            print("Resposta da API (não-JSON):", e.response.text)
        return None
    except Exception as e:
        print(f"\n--- ERRO INESPERADO (Key) ---")
        print(f"Ocorreu um erro: {e}")
        return None

def postar_artigo_na_api_laravel(artigo_final: dict):
    """
    Envia o artigo final gerado pelo "Key" para a API do Laravel.
    """
    print("--- Enviando artigo final para a API Laravel ---")
    
    try:
        response = requests.post(LARAVEL_API_URL, json=artigo_final, timeout=30)
        response.raise_for_status()
        
        # Se chegou aqui, foi 201 Created (ou 200 OK)
        print("\n--- SUCESSO FINAL! ---")
        print("Artigo enviado para o Laravel e guardado como 'rascunho'.")
        print("Pode verificar o 'Painel do Revisor' (painel_ia.html)!")
        print("Resposta da API Laravel:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.HTTPError as e:
        print(f"\n--- ERRO AO ENVIAR PARA O LARAVEL ---")
        print(f"A API Laravel retornou um erro: {e}")
        try:
            print("Resposta da API:", e.response.json())
        except json.JSONDecodeError:
            print("Resposta da API (não-JSON):", e.response.text)
    except requests.exceptions.RequestException as e:
        print(f"\n--- ERRO DE CONEXÃO (Laravel) ---")
        print(f"Não foi possível conectar à API Laravel em {LARAVEL_API_URL}.")
        print(f"Verifique se o seu ambiente Docker (Laravel) está a rodar. Detalhes: {e}")

# --- Ponto de Entrada Principal (O ORQUESTRADOR) ---
if __name__ == "__main__":
    
    print("=== INICIANDO ORQUESTRADOR DE AGENTES (Júlia, Pedro, Key) ===")
    
    # 1. Chamar Agente Júlia
    dados_julia = agente_julia_buscar_dados(TICKER_PARA_ANALISAR)
    
    # 2. Chamar Agente Pedro
    dados_pedro = agente_pedro_analisar(TICKER_PARA_ANALISAR)
    
    # 3. Verificar se ambos funcionaram
    if dados_julia and dados_pedro:
        
        # 4. Chamar Agente Key
        artigo_gerado = agente_key_escrever(TICKER_PARA_ANALISAR, dados_julia, dados_pedro)
        
        if artigo_gerado:
            
            # 5. Preparar o payload final para o Laravel
            # (Adiciona os dados que faltam: ticker e status)
            artigo_final_laravel = {
                "titulo": artigo_gerado.get("titulo"),
                "conteudo": artigo_gerado.get("conteudo"),
                "recomendacao": artigo_gerado.get("recomendacao"),
                "acao_ticker": TICKER_PARA_ANALISAR,
                "status": "rascunho" # Pronto para o "Fator Humano"
            }
            
            # 6. Enviar para a API Laravel
            postar_artigo_na_api_laravel(artigo_final_laravel)
        else:
            print("Agente 'Key' falhou em redigir o artigo.")
    else:
        print("Falha ao obter dados de 'Júlia' ou 'Pedro'. O processo não pode continuar.")
        
    print("=== ORQUESTRADOR DE AGENTES FINALIZADO ===")

