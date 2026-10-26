import folium
from folium.plugins import FastMarkerCluster
import pandas as pd

print("1. Loading cable landing stations...")
df = pd.read_csv("cable_landing_stations.csv")

# Filter out any rows with missing coordinates
df = df.dropna(subset=["latitude", "longitude"])
print(f"Plotting {len(df)} stations...")

# Initialize base map centered on the Atlantic corridor
m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

# Extract coordinates as a list of [lat, lon] pairs for fast rendering
locations = df[["latitude", "longitude"]].values.tolist()

# Add fast-rendering clusters
FastMarkerCluster(data=locations).add_to(m)

# Save to your local HTML file
m.save("index.html")
print("Success! Created index.html with 1,928 clustered landing points.")