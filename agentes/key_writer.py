import google.generativeai as genai
import requests
import logging
import json
from typing import Optional
from models import ArtigoFinal, StockData, AnaliseSentimento

logger = logging.getLogger("AgenteKey")

class GeminiWriter:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", # <--- VERSÃO CORRETA DA SUA LISTA
            generation_config={"response_mime_type": "application/json"}
        )

    def escrever_artigo(self, dados_julia: StockData, dados_pedro: AnaliseSentimento, ticker: str) -> Optional[ArtigoFinal]:
        logger.info(f"Key está redigindo a matéria sobre {ticker} com perfil sênior...")

        # --- ENGENHARIA DE PROMPT AVANÇADA (Perfil Bloomberg/Valor) ---
        prompt = f"""
        ATUE COMO: Editor-Chefe de um portal de notícias financeiras de alta credibilidade (ex: Bloomberg Línea, Valor Econômico).
        SUA MISSÃO: Escrever uma análise de mercado rápida, sofisticada e baseada em dados.

        --- DADOS TÉCNICOS (Fonte: Agente Júlia) ---
        Ativo: {dados_julia.ticker}
        Preço Atual: R$ {dados_julia.price:.2f}
        Variação (Tendência): {dados_julia.tendencia_longo_prazo}
        Média Móvel (200d): R$ {dados_julia.media_movel_200:.2f}
        Máxima 52 sem: R$ {dados_julia.high_52w:.2f} | Mínima 52 sem: R$ {dados_julia.low_52w:.2f}

        --- DADOS DE SENTIMENTO (Fonte: Agente Pedro) ---
        Sentimento do Mercado: {dados_pedro.sentimento.upper()}
        O que dizem as notícias: "{dados_pedro.resumo}"

        --- DIRETRIZES EDITORIAIS RÍGIDAS ---
        1. TOM DE VOZ: Profissional, analítico, sem gírias, mas direto ao ponto. Use termos de mercado corretamente (bullish, bearish, suporte, resistência).
        2. ESTRUTURA DO TEXTO:
           - Título: Impactante, curto e deve conter o Ticker.
           - Lead (1º parágrafo): O que está acontecendo com o preço agora e o motivo principal (notícias).
           - Análise (2º parágrafo): Compare o preço atual com a Média Móvel de 200 dias. Diga se está esticado ou descontado.
           - Veredito (3º parágrafo): Conclusão rápida para o investidor.
        3. FORMATAÇÃO VISUAL:
           - Use negrito (**texto**) para destacar TODOS os preços e porcentagens citados.
        
        --- FORMATO DE SAÍDA (JSON) ---
        Responda APENAS o JSON abaixo preenchido:
        {{
            "titulo": "Manchete aqui",
            "conteudo": "Texto completo em Markdown aqui",
            "recomendacao": "Compra, Venda ou Neutro"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            resultado = json.loads(response.text)
            
            return ArtigoFinal(
                titulo=resultado['titulo'],
                conteudo=resultado['conteudo'],
                recomendacao=resultado['recomendacao'],
                ticker=ticker
            )
        except Exception as e:
            logger.error(f"Erro na redação do artigo: {e}")
            return None

class APILaravelPublisher:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def publicar(self, artigo: ArtigoFinal) -> bool:
        logger.info(f"Enviando artigo de {artigo.ticker} para o Laravel...")
        try:
            # O .model_dump() do Pydantic já converte tudo para dicionário compatível com JSON
            response = requests.post(self.api_url, json=artigo.model_dump(), timeout=15)
            response.raise_for_status()
            logger.info("✅ Artigo publicado com sucesso!")
            return True
        except Exception as e:
            logger.error(f"❌ Falha ao enviar para Laravel: {e}")
            return False

class KeyAgent:
    def __init__(self, writer: GeminiWriter, publisher: APILaravelPublisher):
        self.writer = writer
        self.publisher = publisher

    def processar_e_publicar(self, ticker: str, dados_julia: StockData, dados_pedro: AnaliseSentimento):
        # 1. Escreve
        artigo = self.writer.escrever_artigo(dados_julia, dados_pedro, ticker)
        
        # 2. Publica (apenas se a escrita funcionou)
        if artigo:
            self.publisher.publicar(artigo)