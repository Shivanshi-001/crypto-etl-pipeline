# Crypto ETL Pipeline

A lightweight ETL (Extract, Transform, Load) data pipeline that ingests live cryptocurrency market data, transforms it using Python and Pandas, stores it in PostgreSQL, and visualizes trends in Power BI.

## Architecture

## What it does

- **Extracts** real-time price, market cap, 24h volume, and % change for the top 10 cryptocurrencies from the CoinGecko public API (no key required)
- **Transforms** raw JSON response into a structured DataFrame using Pandas — handles nulls, renames columns, enforces schema
- **Loads** cleaned data into a PostgreSQL table with timestamps, enabling historical trend analysis
- **Schedules** automatic runs every 5 minutes to continuously build up time-series data
- **Visualizes** price trends, 24h movers, and market cap breakdown in an interactive Power BI dashboard

## Tech Stack

- Python 3.11
- PostgreSQL 16
- Pandas, SQLAlchemy, Requests
- Power BI Desktop

## Database Schema

```sql
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    crypto_name VARCHAR(50),
    symbol VARCHAR(10),
    price DECIMAL(20, 8),
    market_cap DECIMAL(30, 2),
    volume_24h DECIMAL(30, 2),
    price_change_24h DECIMAL(10, 4)
);
```

## Setup

```bash
pip install pandas sqlalchemy psycopg2-binary requests
```

Create the database in PostgreSQL:
```sql
CREATE DATABASE crypto_etl;
```

Update the connection string in `crypto_etl.py`:
```python
engine = create_engine("postgresql://postgres@localhost:5432/crypto_etl")
```

Run the pipeline:
```bash
python crypto_etl.py
```

## Dashboard

Built in Power BI Desktop connected directly to PostgreSQL:
- Bitcoin price trend over time
- 24h % change across all tracked coins
- Average price and market cap per coin table