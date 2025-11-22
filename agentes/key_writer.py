import requests
import json
import logging
import os
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# --- Configuração de Logging ---
logger = logging.getLogger("AgenteKey")

# --- Domínio (DTO) ---
@dataclass
class ArtigoFinal:
    titulo: str
    conteudo: str
    recomendacao: str
    ticker: str
    status: str = "rascunho"

# --- Interfaces (Abstraction Layer) ---
class RedatorIA(ABC):
    @abstractmethod
    def escrever_artigo(self, dados_julia: Dict, dados_pedro: Dict, ticker: str) -> Optional[ArtigoFinal]:
        pass

class PublicadorLaravel(ABC):
    @abstractmethod
    def publicar(self, artigo: ArtigoFinal) -> bool:
        pass

# --- Infraestrutura: Gemini Writer (Implementation) ---
class GeminiWriter(RedatorIA):
    def __init__(self, api_key: str):
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
        self.system_prompt = (
            "Você é 'Key', um jornalista financeiro sênior. "
            "Sua função é sintetizar dados técnicos e sentimento de mercado em um artigo "
            "claro, objetivo e acionável. Escreva em Português do Brasil."
        )

    def escrever_artigo(self, dados_julia: Dict, dados_pedro: Dict, ticker: str) -> Optional[ArtigoFinal]:
        logger.info(f"Key está escrevendo o artigo para {ticker}...")

        # Convertendo os inputs complexos para texto string para o prompt
        contexto_julia = json.dumps(dados_julia, indent=2, ensure_ascii=False)
        contexto_pedro = json.dumps(dados_pedro, indent=2, ensure_ascii=False)

        prompt_usuario = f"""
        Escreva um artigo financeiro sobre {ticker} baseado nestes dados:

        --- DADOS FUNDAMENTAIS (Júlia) ---
        {contexto_julia}

        --- SENTIMENTO DE MERCADO (Pedro) ---
        {contexto_pedro}

        REQUISITOS:
        1. Título: Impactante e curto (max 100 chars).
        2. Conteúdo: Mínimo 3 parágrafos. Use markdown básico.
        3. Recomendação: Apenas uma palavra (Compra, Venda, Neutro).
        
        SAÍDA OBRIGATÓRIA: JSON com as chaves 'titulo', 'conteudo', 'recomendacao'.
        """

        payload = {
            "contents": [{"parts": [{"text": prompt_usuario}]}],
            "systemInstruction": {"parts": [{"text": self.system_prompt}]},
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
            response = requests.post(self.api_url, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
            response.raise_for_status()
            
            # Parse do resultado
            resultado_ia = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
            
            return ArtigoFinal(
                titulo=resultado_ia['titulo'],
                conteudo=resultado_ia['conteudo'],
                recomendacao=resultado_ia['recomendacao'],
                ticker=ticker
            )

        except Exception as e:
            logger.error(f"Erro na geração do texto com Gemini: {e}")
            return None

# --- Infraestrutura: Laravel Publisher (Implementation) ---
class APILaravelPublisher(PublicadorLaravel):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def publicar(self, artigo: ArtigoFinal) -> bool:
        logger.info(f"Enviando artigo de {artigo.ticker} para o Laravel...")
        try:
            payload = asdict(artigo)
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            logger.info("Artigo publicado com sucesso no Laravel!")
            return True
        except Exception as e:
            logger.error(f"Falha ao enviar para Laravel: {e}")
            return False

# --- Application Service: Agente Key ---
class KeyAgent:
    def __init__(self, writer: RedatorIA, publisher: PublicadorLaravel):
        self.writer = writer
        self.publisher = publisher

    def processar_e_publicar(self, ticker: str, dados_julia: Dict, dados_pedro: Dict):
        # 1. Escrever
        artigo = self.writer.escrever_artigo(dados_julia, dados_pedro, ticker)
        
        if not artigo:
            logger.error("Falha na etapa de escrita. Abortando.")
            return

        # 2. Publicar
        sucesso = self.publisher.publicar(artigo)
        
        if sucesso:
            logger.info("Ciclo do Agente Key finalizado com êxito.")
        else:
            logger.warning("Artigo foi escrito, mas falhou na publicação.")