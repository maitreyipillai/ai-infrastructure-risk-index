import io
import pandas as pd
import requests

# Direct raw link to the ATLAS Global Data Center CSV dataset
url = "https://raw.githubusercontent.com/Ringmast4r/Global-Data-Center-Map/main/datacenters.csv"

print("1. Downloading global data center records (ATLAS repository)...")
response = requests.get(url, timeout=20)
response.raise_for_status()

# Read the CSV directly into pandas from memory
df_dc = pd.read_csv(io.StringIO(response.text))
print(f"Total raw facilities retrieved: {len(df_dc)}")

# Inspect the column names
print("\nAvailable columns:")
print(df_dc.columns.tolist())

# Preview top countries with most data centers
if "country" in df_dc.columns:
    print("\n--- Top 10 Countries by Data Center Count ---")
    print(df_dc["country"].value_counts().head(10))

# Save locally to your project directory
df_dc.to_csv("datacenters.csv", index=False)
print("\nSuccess! Saved clean records to datacenters.csv")