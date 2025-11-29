# Usa uma imagem Python leve e moderna
FROM python:3.10-slim

# Define variáveis de ambiente para o Python não travar logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Define a pasta de trabalho
WORKDIR /app

# Instala dependências do sistema (necessário para algumas libs)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 5000 (onde o Flask roda)
EXPOSE 5000

# COMANDO FINAL: Roda a API (api.py)
# Se quiser modo desenvolvimento (ver logs na tela):
CMD ["python", "api.py"]

# Se fosse para produção real (deploy), usaria gunicorn:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app"]