import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

VENUE_DATA_CSV_PATH = "../../data/raw_data/venue_data/hudle_venues_data.csv"
OUTPUT_DATA_FOLDER = "../../data/transformed_data/venue_data/"

venue_df = pd.read_csv(VENUE_DATA_CSV_PATH)
venue_df = venue_df.drop(columns=["venue_link", "city", "address", "lattitude", "longitude", "venue_image_api_url", "hudle_venue_id"])
venue_df["venue_age"] = venue_df["is_new"].apply(lambda x: "New" if x else "Old")

grouped_by_zone_count_df = venue_df.groupby(["locality_zone"]).agg(
    venue_count=("venue_id", "count"),
    court_count=("court_count", "sum")
).reset_index()
grouped_by_zone_count_df.to_csv(OUTPUT_DATA_FOLDER + "grouped_by_zone_count.csv", index=False)

grouped_by_locality= venue_df.groupby(["locality", "venue_age"]).agg(
    venue_count=("venue_id", "count"),
    court_count=("court_count", "sum")
).reset_index()
grouped_by_locality.to_csv(OUTPUT_DATA_FOLDER + "grouped_by_locality.csv", index=False)

grouped_by_zone_df = venue_df.groupby(["locality_zone", "venue_age"]).agg(
    venue_count=("venue_id", "count"),
    court_count=("court_count", "sum")
).reset_index()
grouped_by_zone_df.to_csv(OUTPUT_DATA_FOLDER + "grouped_by_zone.csv", index=False)


# Create a pie chart for grouped_by_zone_count_df using Plotly
fig_pie = px.pie(
    grouped_by_zone_count_df,
    names="locality_zone",
    values="venue_count",
    title="Venue Count Distribution by Locality Zone",
    color_discrete_sequence=["#08306b", "#08519c", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7"]
)

# Show the pie chart
fig_pie.show()

# Create a bar chart using Plotly
fig = px.bar(
    grouped_by_zone_df,
    x="locality_zone",
    y="venue_count",
    color="venue_age",
    title="Venue Count by Locality and Venue Age",
    labels={"venue_count": "Number of Venues", "locality": "Locality"},
    barmode="group",
    color_discrete_map={"New": "royalblue", "Old": "orange"}  # Use better contrasting colors
)
fig.update_layout(
    title_font_size=18,
    xaxis_title="Locality",
    yaxis_title="Number of Venues",
    legend_title="Venue Age",
    template="plotly_white"  # Use a clean and modern template
)


# Create a bar chart for grouped_by_locality using Plotly
fig2 = px.bar(
    grouped_by_locality,
    x="locality",
    y="venue_count",
    color="venue_age",
    title="Venue Count by Locality and Venue Age",
    labels={"venue_count": "Number of Venues", "locality": "Locality"},
    barmode="group",
    color_discrete_map={"New": "royalblue", "Old": "orange"}  # Use better contrasting colors
)
fig2.update_layout(
    title_font_size=18,
    xaxis_title="Locality",
    yaxis_title="Number of Venues",
    legend_title="Venue Age",
    template="plotly_white"  # Use a clean and modern template
)

# Show both plots on the same page

# Create a subplot figure
fig_combined = make_subplots(
    rows=1, cols=2, 
    subplot_titles=("Venue Count by Locality Zone", "Venue Count by Locality")
)

# Add the first figure (grouped_by_zone) to the subplot
for trace in fig.data:
    fig_combined.add_trace(trace, row=1, col=1)

# Add the second figure (grouped_by_locality) to the subplot
for trace in fig2.data:
    fig_combined.add_trace(trace, row=1, col=2)

# Update layout for the combined figure
fig_combined.update_layout(
    title_text="Venue Count Analysis",
    title_font_size=20,
    showlegend=True,
    template="plotly_white"
)

