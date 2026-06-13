# Usa uma imagem oficial e leve do Python
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia APENAS o arquivo de dependências primeiro (isso otimiza o Docker)
COPY requirements.txt .

# Instala as bibliotecas (incluindo o uvicorn que estava faltando)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do seu código
COPY . .