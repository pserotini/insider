# Usar imagem leve do Python
FROM python:3.11-slim

# Criar diretório da aplicação
WORKDIR /app

# Copiar os requirements da API
COPY requirements_api.txt .

# Instalar as libs necessárias
RUN pip install --no-cache-dir -r requirements_api.txt

# Copiar o código da API e os arquivos .pkl
COPY src/ ./src/
COPY notebooks/pickle_files ./notebooks/pickle_files

# Liberar a porta da API
EXPOSE 8000

# Rodar o servidor FastAPI
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
