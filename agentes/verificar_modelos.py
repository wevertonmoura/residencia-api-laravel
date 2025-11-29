import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()
chave = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=chave)

print(f"🔍 Verificando modelos disponíveis para a chave...")

try:
    print("\n--- MODELOS DISPONÍVEIS ---")
    for m in genai.list_models():
        # Filtra apenas modelos que geram texto (ignora os de imagem/embedding)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
except Exception as e:
    print(f"❌ Erro ao listar: {e}")