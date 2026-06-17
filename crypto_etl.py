import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ===== STEP 1: FETCH DATA FROM API =====
def fetch_crypto_data():
    """
    Fetches top 10 cryptocurrencies from CoinGecko API (free, no authentication needed).
    Returns a list of dictionaries with price, market cap, and 24h change.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "sparkline": False
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error if API call fails
    
    data = response.json()
    return data

# ===== STEP 2: TRANSFORM DATA WITH PANDAS =====
def transform_crypto_data(raw_data):
    """
    Takes raw API response and extracts relevant columns.
    Renames them to match database schema.
    """
    records = []
    
    for coin in raw_data:
        record = {
            "crypto_name": coin["name"],
            "symbol": coin["symbol"].upper(),
            "price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "volume_24h": coin["total_volume"],
            "price_change_24h": coin["price_change_percentage_24h"]
        }
        records.append(record)
    
    # Convert list of dicts to Pandas DataFrame
    df = pd.DataFrame(records)
    
    # Handle null values (some coins might not have market cap data)
    df = df.fillna(0)
    
    return df

# ===== STEP 3: LOAD DATA INTO POSTGRESQL =====
def load_to_postgres(df):
    """
    Connects to PostgreSQL database and appends the dataframe.
    SQLAlchemy handles the connection pooling and type mapping.
    """
    # Connection string: postgresql://username:password@host:port/database
    engine = create_engine("postgresql://postgres@localhost:5432/crypto_etl")
    
    # if_exists="append" = add new rows without deleting existing ones
    df.to_sql("crypto_prices", con=engine, if_exists="append", index=False)
    
    print(f"✓ Loaded {len(df)} records at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== MAIN PIPELINE =====
import time

def run_pipeline():
    print("Starting ETL pipeline...")
    
    # Extract
    raw_data = fetch_crypto_data()
    print(f"✓ Fetched {len(raw_data)} cryptocurrencies from CoinGecko")
    
    # Transform
    df = transform_crypto_data(raw_data)
    print(f"✓ Transformed data: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Load
    load_to_postgres(df)
    
    print("✓ ETL pipeline complete!\n")

if __name__ == "__main__":
    print("Scheduler started — running every 5 minutes. Press Ctrl+C to stop.\n")
    while True:
        run_pipeline()
        time.sleep(300)  # 300 seconds = 5 minutes