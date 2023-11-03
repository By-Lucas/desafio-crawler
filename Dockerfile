FROM python:3.9-slim

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copie o código-fonte do projeto
COPY . /app/

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do projeto
COPY requirements.txt /app/

# Atualize o Pip
RUN python -m pip install --upgrade pip

# Instale as dependências e limpe o cache
RUN pip install --no-cache-dir -r requirements.txt

# CMD para executar o aplicativo
CMD ["python", "run.py"]
