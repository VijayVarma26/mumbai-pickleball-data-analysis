import pandas as pd
import folium

# Sample DataFrame (Replace this with your actual data)
data = {
    "Venue": ["Wankhede Stadium", "Brabourne Stadium", "DY Patil Stadium", "Maniac Pickleball Arena | Vile Parle"],
    "Latitude": [18.9389, 18.9362, 19.0434, 19.10494],
    "Longitude": [72.8258, 72.8277, 73.0272, 72.83864]
}

df = pd.DataFrame(data)

# Create a Mumbai map centered around Wankhede Stadium
mumbai_map = folium.Map(location=[18.96, 72.82], zoom_start=12)

# Add venues to the map
for index, row in df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=row["Venue"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mumbai_map)

# Save and display the map
mumbai_map.save("mumbai_cricket_venues.html")
mumbai_map
