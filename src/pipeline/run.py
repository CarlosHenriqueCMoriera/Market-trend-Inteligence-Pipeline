"""Main pipeline orchestration."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.database.schema import create_tables
from src.ingestion.fetch_trends import GoogleTrendsFetcher
from src.transformation.transform import transform_all


def run_pipeline(keywords=None, region="PT"):
    """Run the complete pipeline."""
    logger.info("Starting Market Trends Pipeline...")
    
    # Step 1: Create database tables
    logger.info("Step 1: Creating database tables...")
    create_tables()
    
    # Step 2: Fetch trends data
    logger.info("Step 2: Fetching trends data...")
    if keywords is None:
        keywords = ["iphone"]
    fetcher = GoogleTrendsFetcher()
    fetcher.fetch_to_database(keywords, region)
    
    # Step 3: Transform data
    logger.info("Step 3: Transforming data...")
    transform_all()
    
    logger.info("Pipeline complete!")


if __name__ == "__main__":
    keywords = sys.argv[1:] if len(sys.argv) > 1 else None
    region = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1].startswith("-") else "PT"
    run_pipeline(keywords, region)
