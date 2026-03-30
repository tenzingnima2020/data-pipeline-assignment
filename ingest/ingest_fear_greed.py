import requests
import json
from datetime import datetime
import os

# Create folder if it doesn't exist
os.makedirs("data/bronze/fear_greed", exist_ok=True)

# API call to Alternative.me
url = "https://api.alternative.me/fng/"
params = {
    "limit": 365,
    "format": "json"
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

# Save with timestamp in filename
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/fear_greed/fear_greed_{ts}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Saved {filename}")