FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh
ENTRYPOINT ["/bin/sh", "start.sh"]
