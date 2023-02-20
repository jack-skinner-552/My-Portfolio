import plotly.express as px
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("weather_data.csv",  dtype={"State Codes": str}, encoding = "ISO-8859-1")

# Create the Choropleth map
fig = px.choropleth(df, locations='State Codes', locationmode="USA-states", scope="usa", color='Temperature (°C)', title="Average Temperature by US State", 
    color_continuous_scale="Viridis", hover_data=['Humidity (%)', 'Pressure (mb)'], hover_name='State', custom_data=['State', 'Humidity (%)', 'Pressure (mb)'])

# Customize the hover label template
fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Temperature: %{z}°C<br>Humidity: %{customdata[1]}<br>Pressure: %{customdata[2]}')

# Show the map
fig.show()