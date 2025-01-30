import json
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
from collections import Counter

# Load JSON data
with open("MyDataBroker/miniIp.json", "r") as file:
    data = json.load(file)

# Count occurrences of each location
location_counts = Counter(entry["loc"] for entry in data)

# Extract unique locations with visit counts
locations = []
for loc, count in location_counts.items():
    lat, lon = map(float, loc.split(","))  # Convert "lat,lon" string to float values
    locations.append({"city": data[0]["city"], "geometry": Point(lon, lat), "count": count})

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(locations, crs="EPSG:4326")  # WGS84 Lat/Lon

# Convert to Web Mercator (EPSG:3857) for `contextily`
gdf = gdf.to_crs(epsg=3857)

# Scale dot size based on visit count
gdf["size"] = gdf["count"] * 100  # Adjust factor for better visibility
gdf["label_size"] = gdf["count"] * 2  # Adjust factor for readable labels

# Create larger figure
fig, ax = plt.subplots(figsize=(12, 8))

# Plot locations with scaled markers
gdf.plot(ax=ax, color="red", alpha=0.7, markersize=gdf["size"], label="Locations")

# Add city labels with scaled font sizes
for _, row in gdf.iterrows():
    ax.text(row.geometry.x, row.geometry.y, row.city, fontsize=row["label_size"], ha='right')

# Add basemap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.HOT)



# Customize plot
ax.set_title("Locations from JSON Data on a Map (Scaled by Visits)")
ax.legend()
plt.show()

