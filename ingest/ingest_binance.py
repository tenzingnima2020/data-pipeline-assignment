import requests
import json
from datetime import datetime
import os

# Create folder if it doesn't exist
os.makedirs("data/bronze/binance", exist_ok=True)

# API call to Binance
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "1d",
    "limit": 365
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

# Save with timestamp in filename
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/binance/btc_klines_{ts}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")