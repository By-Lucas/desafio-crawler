import psycopg2
from loguru import logger
from decouple import config


db_params = {
    "database": config("DB_NAME"),
    "user": config("DB_USER"),
    "password": config("DB_PASSWORD"),
    "host": config("DB_HOST"),
    "port": config("DB_PORT"),  # Porta padrão do PostgreSQL
}

create_table_sql = """
CREATE TABLE IF NOT EXISTS beemon_bot (
    id SERIAL PRIMARY KEY,
    text TEXT,
    author TEXT,
    born TEXT,
    location TEXT,
    tags TEXT,
    description TEXT
);
"""

def create_database_table():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Tabela 'beemon_bot' criada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar a tabela no PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()


def record_exists(cursor, text, author):
    # Consulta SQL para verificar se um registro com o mesmo texto e autor já existe
    query = "SELECT id FROM beemon_bot WHERE text = %s AND author = %s"
    cursor.execute(query, (text, author))
    return cursor.fetchone() is not None

def save_data_to_postgresql(data):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        for quote in data:
            text = quote["text"]
            author = quote["Author"]
            born = quote["Born"]
            location = quote["Location"]
            tags = quote["Tags"]
            description = quote["Description"]

            if not record_exists(cursor, text, author):
                insert_query = "INSERT INTO beemon_bot (text, author, born, location, tags, description) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (text, author, born, location, tags, description)
                cursor.execute(insert_query, values)

        conn.commit()
        logger.success("Dados salvo no banco de dados")
    except Exception as e:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()