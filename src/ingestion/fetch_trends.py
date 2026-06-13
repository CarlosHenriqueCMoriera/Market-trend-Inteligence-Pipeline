import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from pytrends.request import TrendReq
from dotenv import load_dotenv
from loguru import logger
import psycopg2

# Load environment variables
load_dotenv()


class GoogleTrendsFetcher:
    """Fetch Google Trends data for given keywords."""
    
    def __init__(self, hl="pt-PT", tz=0):
        self.pytrends = TrendReq(hl=hl, tz=tz)
    
    def fetch(self, keywords, timeframe="today 3-m", region="PT"):
        """Fetch trends for given keywords."""
        data = {}
        for keyword in keywords:
            self.pytrends.build_payload([keyword], timeframe=timeframe)
            df = self.pytrends.interest_over_time()
            if not df.empty:
                data[keyword] = df[keyword].to_dict()
        return data
    
    def fetch_to_database(self, keywords, region="PT"):
        """Fetch and insert data into database."""
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "market_trends"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        
        trends_data = self.fetch(keywords, region=region)
        
        for keyword, values in trends_data.items():
            for date, value in values.items():
                cursor.execute(
                    """INSERT INTO raw_trends (keyword, value, date, region)
                       VALUES (%s, %s, %s, %s)""",
                    (keyword, value, date.date(), region)
                )
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Dados inseridos para keywords: {keywords}")


def main():
    """CLI entry point."""
    keywords = ["iphone"]  # Default keywords
    if len(sys.argv) > 1:
        keywords = sys.argv[1:]
    
    fetcher = GoogleTrendsFetcher()
    fetcher.fetch_to_database(keywords)


if __name__ == "__main__":
    main()
