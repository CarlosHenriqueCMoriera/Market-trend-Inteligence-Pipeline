"""Data transformation module."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger
import psycopg2

load_dotenv()


def clean_null_values():
    """Remove records with null values."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        delete from raw_trends 
        where value is null or keyword is null
    """)
    
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Deleted {deleted} records with null values")
    return deleted


def deduplicate():
    """Remove duplicate records."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        delete from raw_trends 
        where id not in (
            select min(id) 
            from raw_trends 
            group by keyword, date, region
        )
    """)
    
    deleted = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Deleted {deleted} duplicate records")
    return deleted


def transform_all():
    """Run all transformations."""
    logger.info("Starting transformations...")
    clean_null_values()
    deduplicate()
    logger.info("Transformations complete!")


if __name__ == "__main__":
    transform_all()
