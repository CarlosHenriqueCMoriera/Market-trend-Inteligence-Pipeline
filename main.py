#!/usr/bin/env python3
"""Market Trends Intelligence Pipeline CLI."""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.database.schema import create_tables
from src.ingestion.fetch_trends import GoogleTrendsFetcher
from src.transformation.transform import transform_all

# Remove default logger
logger.remove()

# Add custom logger
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Market Trends Intelligence Pipeline"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=["iphone"],
        help="Keywords to track (default: iphone)"
    )
    parser.add_argument(
        "--region",
        default="PT",
        help="Region code (default: PT)"
    )
    parser.add_argument(
        "--timeframe",
        default="today 3-m",
        help="Timeframe for trends (default: today 3-m)"
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip data fetching"
    )
    parser.add_argument(
        "--skip-transform",
        action="store_true",
        help="Skip data transformation"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting Market Trends Pipeline...")
    
    # Step 1: Create database tables
    logger.info("Step 1: Creating database tables...")
    create_tables()
    
    # Step 2: Fetch trends data
    if not args.skip_fetch:
        logger.info("Step 2: Fetching trends data...")
        fetcher = GoogleTrendsFetcher()
        fetcher.fetch_to_database(args.keywords, args.region)
    else:
        logger.info("Step 2: Skipping data fetch...")
    
    # Step 3: Transform data
    if not args.skip_transform:
        logger.info("Step 3: Transforming data...")
        transform_all()
    else:
        logger.info("Step 3: Skipping transformation...")
    
    logger.info("Pipeline complete!")


if __name__ == "__main__":
    main()
