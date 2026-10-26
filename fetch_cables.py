import pandas as pd
import requests

url = "https://www.submarinecablemap.com/api/v3/landing-point/landing-point-geo.json"

print("Downloading subsea cable landing data...")
response = requests.get(url)
data = response.json()

features = data["features"]
print(f"Total global landing points found: {len(features)}")

landing_list = []
for item in features:
    coords = item["geometry"]["coordinates"]
    props = item["properties"]
    full_name = props.get("name", "")

    # Extract the country name: "Cork, Ireland" -> "Ireland"
    if "," in full_name:
        country = full_name.split(",")[-1].strip()
    else:
        country = full_name.strip()

    landing_list.append(
        {
            "id": props.get("id"),
            "name": full_name,
            "country": country,
            "longitude": coords[0],
            "latitude": coords[1],
        }
    )

df = pd.DataFrame(landing_list)

print("\n--- Top 10 Countries by Subsea Cable Landing Points ---")
print(df["country"].value_counts().head(10))

# Save the updated, clean CSV
df.to_csv("cable_landing_stations.csv", index=False)
print("\nSuccess! Saved clean dataset with parsed countries to cable_landing_stations.csv")