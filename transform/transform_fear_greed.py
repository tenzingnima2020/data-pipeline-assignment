import json
import pandas as pd
import glob
import os

# Find the most recent bronze file
files = glob.glob("data/bronze/fear_greed/*.json")
latest_file = max(files)
print(f"Reading: {latest_file}")

# Load raw data
with open(latest_file, "r") as f:
    raw = json.load(f)

# Convert to dataframe
df = pd.DataFrame(raw["data"])

# Clean and transform
df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms").dt.date
df["fear_greed_value"] = df["value"].astype(int)
df["fear_greed_label"] = df["value_classification"]

# Keep only clean columns
silver = df[["date", "fear_greed_value", "fear_greed_label"]]

# Save to silver
os.makedirs("data/silver", exist_ok=True)
silver.to_csv("data/silver/fear_greed_clean.csv", index=False)
print(f"✅ Saved data/silver/fear_greed_clean.csv with {len(silver)} rows")