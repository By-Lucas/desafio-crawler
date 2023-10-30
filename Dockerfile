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

# Atualiza o Pip
RUN python -m pip install --upgrade pip

# Instale o Celery e suas dependências, incluindo o Celery Beat
RUN pip install celery==5.1.0 celery[beat]

# Limpa o cache e remove dependências
RUN pip install --no-cache-dir -r requirements.txt

# CMD para executar o Celery Beat
CMD ["celery", "-A", "config.celery", "beat", "--loglevel=INFO"]

