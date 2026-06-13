# Market Trends Intelligence Pipeline


A production-ready data pipeline for collecting, storing, and analyzing Google Trends data for market intelligence.

> Built as part of a Data Engineering portfolio to demonstrate ETL pipeline design, database modeling, and analytical workflows using real-world tools and best practices.

---

## Overview

This pipeline fetches search trend data from Google Trends API, stores it in PostgreSQL, and provides analytical models via dbt for business insights.

---

## Features

- Automated Google Trends data collection
- PostgreSQL data storage with schema management
- Data cleaning and deduplication
- dbt models for analytics (staging + marts)
- CLI interface with flexible options
- Comprehensive test suite

---

## Tech Stack

- **Language**: Python 3.8+
- **Database**: PostgreSQL
- **ETL**: dbt (Data Build Tool)
- **Logging**: Loguru
- **API**: Google Trends (pytrends)

---

## Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/CarlosHenriqueCMoriera/Market-trend-Inteligence-Pipeline.git
cd Market-trend-Inteligence-Pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
vim .env
```

### 3. Create Database

```bash
createdb market_trends
```

### 4. Run Pipeline

```bash
# Full pipeline
python main.py --keywords iphone android samsung

# Fetch only
python main.py --keywords iphone --skip-transform

# Transform only
python main.py --skip-fetch
```

---

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--keywords` | Keywords to track | `iphone` |
| `--region` | Region code | `PT` |
| `--timeframe` | Trend timeframe | `today 3-m` |
| `--skip-fetch` | Skip data fetch | `false` |
| `--skip-transform` | Skip transformation | `false` |

---

## Project Structure

```
Market-trend-Inteligence-Pipeline/
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .env.example                # Environment template
├── README.md                   # This file
├── src/
│   ├── database/
│   │   ├── connection.py       # PostgreSQL connection
│   │   └── schema.py           # Table definitions
│   ├── ingestion/
│   │   └── fetch_trends.py     # Google Trends fetcher
│   ├── transformation/
│   │   └── transform.py        # Data cleaning
│   └── pipeline/
│       └── run.py              # Orchestration
├── dbt/
│   ├── dbt_project.yml         # dbt configuration
│   ├── analysis/               # dbt manifest
│   └── models/
│       ├── staging/            # Staging models
│       │   └── stg_raw_trends.sql
│       └── marts/              # Analytics models
│           ├── fct_daily_trends.sql
│           └── fct_keyword_stats.sql
└── tests/
    └── test_pipeline.py        # Test suite
```

---

## Database Schema

### raw_trends

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| keyword | VARCHAR(100) | NOT NULL | Search keyword |
| value | INTEGER | NOT NULL | Trend index (0-100) |
| date | DATE | NOT NULL | Data date |
| region | VARCHAR(10) | NOT NULL | Geographic code |
| collected_at | TIMESTAMP | DEFAULT NOW() | Collection time |

---

## dbt Models

### Staging Layer
- `stg_raw_trends` — Cleaned raw data view

### Marts Layer
- `fct_daily_trends` — Daily trends with 7-day moving average
- `fct_keyword_stats` — Aggregated keyword statistics

---

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Running dbt

```bash
cd dbt
dbt debug
dbt run
dbt test
```

---

## License

MIT License — see LICENSE file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

