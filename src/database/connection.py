import psycopg2
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        logger.info("Conexão com PostgreSQL estabelecida com sucesso!")
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar com PostgreSQL: {e}")
        raise

if __name__ == "__main__":
    conn = get_connection()
    conn.close()
    