FROM python:3.9-slim

# Install the PostgreSQL development libraries and build tools
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

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

# Limpa o cache e remove dependências
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint de inicialização do app
RUN chmod +x start.sh
ENTRYPOINT ["/bin/sh", "start.sh"]