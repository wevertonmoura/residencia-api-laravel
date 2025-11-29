import google.generativeai as genai
import logging
import json
from typing import Optional
from models import AnaliseSentimento, FonteInfo

logger = logging.getLogger("AgentePedro")

def find_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

class GeminiProvider:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        
        # Usamos o modelo que sabemos que funciona na sua conta
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def analisar_mercado(self, ticker: str) -> Optional[AnaliseSentimento]:
        logger.info(f"Pedro analisando (Análise Fundamentalista): {ticker}...")
        
        # Prompt focado em conhecimento técnico, já que desligamos a busca externa
        prompt = (
            f"Atue como um analista financeiro Sênior. "
            f"Com base no seu vasto conhecimento sobre o mercado brasileiro, analise a ação {ticker}. "
            f"Considere o histórico da empresa, setor e fundamentos. "
            f"Responda EXCLUSIVAMENTE um JSON: "
            f"{{'sentimento': 'Positivo/Negativo/Neutro', 'resumo': 'Análise técnica baseada em fundamentos e histórico recente.'}}"
        )

        try:
            # REMOVEMOS A PARTE 'TOOLS' PARA EVITAR O ERRO
            response = self.model.generate_content(prompt)
            
            texto_limpo = find_json(response.text)
            dados_ia = json.loads(texto_limpo)
            
            return AnaliseSentimento(
                ticker=ticker,
                sentimento=dados_ia.get("sentimento", "Neutro"),
                resumo=dados_ia.get("resumo", "Sem dados"),
                fontes=[] # Sem busca, sem fontes externas
            )

        except Exception as e:
            logger.error(f"❌ Erro fatal no Pedro: {e}")
            return None

class PedroAgent:
    def __init__(self, provider: GeminiProvider):
        self.provider = provider

    def execute(self, ticker: str) -> Optional[AnaliseSentimento]:
        return self.provider.analisar_mercado(ticker)