import pandas as pd
import os

# Read silver datasets
btc = pd.read_csv("data/silver/btc_daily_clean.csv")
fg = pd.read_csv("data/silver/fear_greed_clean.csv")

# Convert date columns to same type
btc["date"] = pd.to_datetime(btc["date"])
fg["date"] = pd.to_datetime(fg["date"])

# Join on date
gold = pd.merge(btc, fg, on="date", how="inner")

# Sort by date
gold = gold.sort_values("date").reset_index(drop=True)

# Create derived columns
gold["btc_daily_return"] = gold["btc_close"].pct_change() * 100
gold["positive_return"] = (gold["btc_daily_return"] > 0).astype(int)
gold["is_weekend"] = pd.to_datetime(gold["date"]).dt.dayofweek >= 5

#Deleting rows with missing values
gold = gold.dropna()

# Save to gold
os.makedirs("data/gold", exist_ok=True)
gold.to_csv("data/gold/crypto_sentiment_daily.csv", index=False)
print(f"Saved data/gold/crypto_sentiment_daily.csv with {len(gold)} rows")
print(gold.head())