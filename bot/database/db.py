import psycopg2
from loguru import logger


db_params = {
    "database": "beemon_bot",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432,  # Porta padrão do PostgreSQL
}

# Definição da tabela
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
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Tabela 'beemon_bot' criada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar a tabela no PostgreSQL: {e}")
    finally:
        conn.close()


def save_data_to_postgresql(data):
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

            # Substitua o nome da tabela pelo nome da sua tabela no PostgreSQL
            insert_query = "INSERT INTO beemon_bot (text, author, born, location, tags, description) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (text, author, born, location, tags, description)

            cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
    except Exception as e:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {e}")
    finally:
        conn.close()
