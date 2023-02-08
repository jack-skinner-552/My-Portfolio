import plotly.express as px
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("weather_data.csv",  dtype={"State Codes": str}, encoding = "ISO-8859-1")

# Create the Choropleth map
fig = px.choropleth(df, locations='State Codes', locationmode="USA-states", scope="usa", color='Temperature (°C)', title="Average Temperature by US State",
                    color_continuous_scale="Viridis")

# Show the map
fig.show()