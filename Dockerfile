# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requirements.txt para o container
COPY requirements.txt requirements.txt

# Copiar todo o diretório src/doc para o diretório de trabalho no container
COPY src/doc /app/src/doc

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Taipy vai usar (geralmente 5000)
EXPOSE 5000

# Definir o comando para rodar a aplicação
CMD ["python", "src/doc/main.py"]
