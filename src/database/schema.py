from .connection import get_connection
from loguru import logger

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_trends (
            id SERIAL PRIMARY KEY,
            keyword VARCHAR(100),
            value INTEGER,
            date DATE,
            region VARCHAR(10),
            collected_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Tabela criada com sucesso!")

if __name__ == "__main__":
    create_tables()
