import requests
import json
import logging
import re
import os
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod

# --- 1. Configuração de Logging e Constantes ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentePedro")

# Configuração da API (Idealmente, use variáveis de ambiente em produção)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC9HLiKBIf-8fmQmqbc5uTHbPra-jx8xV8")
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"

# --- 2. Entidades de Domínio (Domain Layer) ---
@dataclass
class FonteInfo:
    titulo: str
    uri: str

@dataclass
class AnaliseSentimento:
    ticker: str
    sentimento: str  # Positivo, Negativo, Neutro
    resumo: str
    fontes: List[FonteInfo] = field(default_factory=list)

# --- 3. Interface do Provedor de IA (Abstraction) ---
class LLMProvider(ABC):
    @abstractmethod
    def analisar_mercado(self, ticker: str) -> Optional[AnaliseSentimento]:
        pass

# --- 4. Implementação do Gemini (Infrastructure Layer) ---
class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        self.system_prompt = (
            "Você é 'Pedro', um analista de sentimento de mercado. "
            "Sua função é analisar notícias recentes sobre uma ação. "
            "Sua resposta DEVE conter APENAS um bloco de código JSON válido."
        )

    def _extract_json(self, text: str) -> str:
        """Limpa a resposta da IA para extrair apenas o JSON."""
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return match.group(1)
        
        text = text.strip()
        if text.startswith('{') and text.endswith('}'):
            return text
        raise ValueError("JSON não encontrado na resposta da IA")

    def analisar_mercado(self, ticker: str) -> Optional[AnaliseSentimento]:
        logger.info(f"Solicitando análise ao Gemini para: {ticker}")
        
        user_prompt = (
            f"Analise o sentimento atual do mercado (Positivo, Negativo ou Neutro) para a ação {ticker}, "
            f"com base nas notícias mais recentes encontradas via Google Search. "
            f"Retorne um JSON com as chaves: 'sentimento' e 'resumo_analise' (em português)."
        )

        payload = {
            "contents": [{"parts": [{"text": user_prompt}]}],
            "systemInstruction": {"parts": [{"text": self.system_prompt}]},
            "tools": [{"google_search": {}}], # Ativa a busca do Google
        }

        try:
            response = requests.post(
                self.url, 
                json=payload, 
                headers={"Content-Type": "application/json"}, 
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

            # Processamento da Resposta
            candidate = data['candidates'][0]
            raw_text = candidate['content']['parts'][0]['text']
            
            # Parsing do JSON da IA
            json_text = self._extract_json(raw_text)
            parsed_data = json.loads(json_text)

            # Extração de Fontes (Grounding)
            fontes_lista = []
            if 'groundingMetadata' in candidate and 'groundingAttributions' in candidate['groundingMetadata']:
                for attr in candidate['groundingMetadata']['groundingAttributions']:
                    if 'web' in attr:
                        fontes_lista.append(FonteInfo(
                            titulo=attr['web'].get('title', 'Sem título'),
                            uri=attr['web'].get('uri', '#')
                        ))

            return AnaliseSentimento(
                ticker=ticker,
                sentimento=parsed_data.get("sentimento", "Neutro"),
                resumo=parsed_data.get("resumo_analise", "Sem resumo disponível."),
                fontes=fontes_lista
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão com Gemini API: {e}")
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Erro ao processar resposta da IA: {e}")
            # Em produção, poderíamos logar o raw_text aqui para debug
        except Exception as e:
            logger.error(f"Erro inesperado no GeminiProvider: {e}")
        
        return None

# --- 5. O Agente Pedro (Application Layer) ---
class PedroAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def execute(self, ticker: str) -> Optional[Dict[str, Any]]:
        logger.info("--- Agente Pedro Iniciando ---")
        
        analise = self.provider.analisar_mercado(ticker)
        
        if not analise:
            logger.warning(f"Não foi possível concluir a análise para {ticker}.")
            return None

        logger.info("Análise de sentimento concluída com sucesso.")
        
        # Formata para retorno (dicionário limpo)
        return {
            "agente": "Pedro",
            "ticker": analise.ticker,
            "analise": {
                "sentimento": analise.sentimento,
                "resumo_analise": analise.resumo
            },
            "fontes": [asdict(f) for f in analise.fontes]
        }

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Injeção de Dependência
    gemini_provider = GeminiProvider(api_key=GEMINI_API_KEY, model=GEMINI_MODEL)
    agente_pedro = PedroAgent(provider=gemini_provider)

    # Execução
    resultado = agente_pedro.execute("PETR4.SA")
    
    if resultado:
        print("\n--- Resultado Final (Pedro) ---")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))