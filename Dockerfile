# Usar uma imagem base do Python
FROM python:3.12

# Instalar pacotes do sistema operacional necessários
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY requirements.txt requirements.txt
COPY src/doc /app/src/doc

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Taipy vai usar (geralmente 5000)
EXPOSE 5000

# Definir o comando para rodar a aplicação
CMD ["python", "src/doc/main.py"]