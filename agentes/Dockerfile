# Usa uma imagem Python leve
FROM python:3.10-slim

# Define a pasta de trabalho DENTRO do container
WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da pasta agentes para dentro do container
COPY . .

# Garante que o Python não bufferize a saída (para vermos os logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Comando padrão (deixa o container vivo esperando comandos)
CMD ["tail", "-f", "/dev/null"]