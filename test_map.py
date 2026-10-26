import folium

# Initialize a world map using OpenStreetMap (100% free, no API key needed)
m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

# Add a test pin for Singapore
folium.Marker(
    location=[1.3521, 103.8198],
    popup="<b>Singapore Hub</b><br>Critical Subsea Transit Chokepoint",
    tooltip="Click for details",
).add_to(m)

# Save the map
m.save("index.html")
print("Success! Created index.html with free OpenStreetMap tiles.")