# ============================================================
# Merging the old Gold dataset with cleaned Google Trends daily data
# ============================================================

import pandas as pd
from pathlib import Path

# CHANGE THIS to match your real old Gold file name
old_gold_file = Path(r"C:\Users\A S U S\aidi-1204-Assignment3\data\gold\crypto_sentiment_daily.csv")

# Google Trends cleaned file
trends_file = Path(r"C:\Users\A S U S\aidi-1204-Assignment3\data\silver\google_trends_bitcoin_clean.csv")

# New output file
new_gold_file = Path(r"C:\Users\A S U S\aidi-1204-Assignment3\data\gold\final_dataset_v2.csv")

# 1. Read files
gold_df = pd.read_csv(old_gold_file)
trends_df = pd.read_csv(trends_file)

print("Old Gold columns:")
print(gold_df.columns.tolist())

print("\nTrends columns:")
print(trends_df.columns.tolist())

# 2. Convert dates
gold_df["date"] = pd.to_datetime(gold_df["date"], errors="coerce")
trends_df["date"] = pd.to_datetime(trends_df["date"], errors="coerce")

# 3. Merge on date
merged = gold_df.merge(trends_df, on="date", how="left")

# 4. Fill missing Google Trends values
merged["google_trends_bitcoin"] = merged["google_trends_bitcoin"].ffill().bfill()

# 5. Create new derived variables
median_trend = merged["google_trends_bitcoin"].median()

merged["high_interest_day"] = (
    merged["google_trends_bitcoin"] > median_trend
).astype(int)

merged["interest_group"] = merged["high_interest_day"].map({
    0: "Low Interest",
    1: "High Interest"
})

# Optional extra variable
if "btc_daily_return" in merged.columns:
    merged["abs_return"] = merged["btc_daily_return"].abs()

# 6. Save new Gold dataset
new_gold_file.parent.mkdir(parents=True, exist_ok=True)
merged.to_csv(new_gold_file, index=False)

print("\nNew Gold dataset saved to:")
print(new_gold_file)
print(merged.head())
print("\nFinal columns:")
print(merged.columns.tolist())