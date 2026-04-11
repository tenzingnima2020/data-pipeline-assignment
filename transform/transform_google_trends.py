# ============================================================
# Convert weekly Google Trends CSV into daily clean data
# ============================================================

import pandas as pd
from pathlib import Path

# File paths
input_file = Path("data/bronze/google_trends/google_trends_bitcoin_raw.csv")
output_file = Path("data/silver/google_trends_bitcoin_clean.csv")

# 1. Read raw CSV
df = pd.read_csv(input_file)

print("Raw columns:")
print(df.columns.tolist())
print(df.head())

# 2. Rename columns
# Change these if your file uses different names
df = df.rename(columns={
    "date": "date",
    "bitcoin": "google_trends_bitcoin",
    "Time": "date"
})

# If the file still has 'bitcoin' in lower case, this keeps it correct
if "google_trends_bitcoin" not in df.columns and "bitcoin" in df.columns:
    df = df.rename(columns={"bitcoin": "google_trends_bitcoin"})

# 3. Keep only needed columns
df = df[["date", "google_trends_bitcoin"]].copy()

# 4. Convert types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["google_trends_bitcoin"] = pd.to_numeric(df["google_trends_bitcoin"], errors="coerce")

# 5. Drop bad rows
df = df.dropna(subset=["date", "google_trends_bitcoin"])

# 6. Sort
df = df.sort_values("date").reset_index(drop=True)

print("\nWeekly Google Trends data:")
print(df.head())

# 7. Expand weekly data into daily data
daily_rows = []

for i in range(len(df)):
    start_date = df.loc[i, "date"]
    trend_value = df.loc[i, "google_trends_bitcoin"]

    if i < len(df) - 1:
        end_date = df.loc[i + 1, "date"] - pd.Timedelta(days=1)
    else:
        end_date = start_date + pd.Timedelta(days=6)

    all_days = pd.date_range(start=start_date, end=end_date, freq="D")

    for single_day in all_days:
        daily_rows.append({
            "date": single_day,
            "google_trends_bitcoin": trend_value
        })

daily_df = pd.DataFrame(daily_rows)

# 8. Clean final daily data
daily_df = daily_df.drop_duplicates(subset=["date"])
daily_df = daily_df.sort_values("date").reset_index(drop=True)
daily_df["date"] = daily_df["date"].dt.strftime("%Y-%m-%d")

# 9. Save to Silver
output_file.parent.mkdir(parents=True, exist_ok=True)
daily_df.to_csv(output_file, index=False)

print("\nDaily cleaned Google Trends data saved to:")
print(output_file)
print(daily_df.head(15))
print(daily_df.tail(10))
print("\nShape:", daily_df.shape)