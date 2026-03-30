import json
import pandas as pd
import glob
import os

# Find the most recent bronze file
files = glob.glob("data/bronze/binance/*.json")
latest_file = max(files)
print(f"Reading: {latest_file}")

# Load raw data
with open(latest_file, "r") as f:
    raw = json.load(f)

# Convert to dataframe
df = pd.DataFrame(raw, columns=[
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "num_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
])

# Clean and transform
df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.date
df["btc_close"] = df["close"].astype(float)
df["btc_volume"] = df["volume"].astype(float)
df["btc_high"] = df["high"].astype(float)
df["btc_low"] = df["low"].astype(float)

# Keep only clean columns
silver = df[["date", "btc_close", "btc_volume", "btc_high", "btc_low"]]

# Save to silver
os.makedirs("data/silver", exist_ok=True)
silver.to_csv("data/silver/btc_daily_clean.csv", index=False)
print(f"✅ Saved data/silver/btc_daily_clean.csv with {len(silver)} rows")