# data-pipeline-assignment
Data pipeline for crypto sentiment analysis

# Data Pipeline Assignment — Part 1

## Overview
This project builds a data pipeline that pulls crypto market data
and sentiment data from public APIs, stores raw snapshots locally,
and transforms the data into a clean, analysis-ready Gold dataset
using a medallion architecture: Bronze → Silver → Gold.

## API Pack
Pack A — Crypto & Sentiment
- Binance Market Data API (daily BTC OHLCV)
- Alternative.me Fear & Greed Index (daily sentiment score)

## Architecture
```
Public APIs → Bronze (raw JSON) → Silver (cleaned CSV) → Gold (joined CSV)
```

## Folder Structure
```
data/bronze/   ← raw API snapshots
data/silver/   ← cleaned, typed tables
data/gold/     ← analysis-ready dataset
ingest/        ← API ingestion scripts
transform/     ← cleaning and joining scripts
notebooks/     ← (reserved for Part 2)
```

## How to Run

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run ingestion (Bronze)
```
python ingest/ingest_binance.py
python ingest/ingest_fear_greed.py
```

### 3. Run transforms (Silver)
```
python transform/transform_binance.py
python transform/transform_fear_greed.py
```

### 4. Create Gold dataset
```
python transform/create_gold.py
```

## Gold Dataset Columns
| Column | Description |
|--------|-------------|
| date | Trading date |
| btc_close | BTC closing price |
| btc_volume | BTC trading volume |
| btc_high | BTC daily high |
| btc_low | BTC daily low |
| fear_greed_value | Sentiment score (0-100) |
| fear_greed_label | Sentiment label (Fear/Greed) |
| btc_daily_return | % price change day over day |
| positive_return | 1 if return was positive, else 0 |
| is_weekend | True if Saturday or Sunday |

## AI Usage
- Used GitHub Copilot to help write boilerplate API request code
- Used ChatGPT to help debug the Fear & Greed timestamp conversion
- Had to verify and fix the timestamp unit manually (ms vs s)
  by inspecting the raw JSON values from the API response
