FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install psycopg2-binary

COPY . .

COPY start.sh .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
