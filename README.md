# Market Trends Intelligence Pipeline

A data pipeline that collects, stores, and analyzes Google Trends data for market intelligence.

## Features

- Fetch Google Trends data for multiple keywords
- Store data in PostgreSQL
- Data cleaning and transformation
- dbt models for analytics
- CLI interface

## Requirements

- Python 3.8+
- PostgreSQL
- dbt

## Installation

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. Create database:
   ```bash
   createdb market_trends
   ```

## Usage

### CLI

Run the pipeline:
```bash
python main.py --keywords iphone android samsung
```

Options:
- `--keywords`: Keywords to track (default: iphone)
- `--region`: Region code (default: PT)
- `--timeframe`: Timeframe for trends (default: today 3-m)
- `--skip-fetch`: Skip data fetching
- `--skip-transform`: Skip data transformation

### Python

```python
from src.pipeline.run import run_pipeline

run_pipeline(keywords=["iphone"], region="PT")
```

### Fetch Trends Only

```bash
python -m src.ingestion.fetch_trends iphone
```


### Transform Only

```bash
python -m src.transformation.transform
```


## Project Structure

```
market_trends/
├── main.py              # CLI entry point
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── src/
│   ├── database/      # Database connection & schema
│   ├── ingestion/     # Google Trends fetching
│   ├── transformation/# Data cleaning
│   └── pipeline/       # Pipeline orchestration
├── dbt/                # dbt models
│   ├── models/
│   │   ├── staging/  # Staging models
│   │   └── marts/     # Analytical models
│   └── 分析/           # dbt configuration
└── tests/              # Test suite
```

## Database Schema

### raw_trends

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| keyword | VARCHAR(100) | Search keyword |
| value | INTEGER | Trend index value |
| date | DATE | Date of data point |
| region | VARCHAR(10) | Geographic region |
| collected_at | TIMESTAMP | Collection timestamp |

## dbt Models

### Staging
- `stg_raw_trends`: Clean raw data view

### Marts
- `fct_daily_trends`: Daily trends with moving averages
- `fct_keyword_stats`: Keyword statistics summary

## License

MIT
