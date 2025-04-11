# Use a imagem oficial do Python
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Criar e definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primeiro para aproveitar o cache de camadas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o projeto inteiro
COPY . .

# Porta que o Django usa
EXPOSE 8000

# Comando para rodar o servidor (com as migrações e setup inicial)
CMD ["sh", "-c", \
    "python manage.py makemigrations && \
     python manage.py migrate && \
     python manage.py setup_initial_data && \
     python manage.py runserver 0.0.0.0:8000"]
