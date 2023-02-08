import requests
import csv
import plotly.express as px
import pandas as pd

# API endpoint to get weather information
endpoint = "http://api.weatherstack.com/current"

# API key to access the data
api_key = "584d10983c5faf9b551fae1c3895d88c"

# list of all 50 US states
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
          "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
          "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
          "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
          "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
          "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
          "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
          "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
          "Washington", "West Virginia", "Wisconsin", "Wyoming"]

state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN",
               "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
               "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
               "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
# headers for the CSV file
headers = ["State", "State Codes", "Temperature", "Humidity (%)", "Pressure (mb)"]

# data to be stored in the CSV file
data = []

# loop through all 50 states and get weather information
for state, state_code in zip(states, state_codes):
    # API query parameters
    params = {
        "access_key": api_key,
        "query": state
    }

    # make API request and get the response
    response = requests.get(endpoint, params=params)
    response_json = response.json()

    # extract weather information from the response
    temperature = response_json["current"]["temperature"]
    humidity = response_json["current"]["humidity"]
    pressure = response_json["current"]["pressure"]

    # add the weather information to the data list
    data.append([state, state_code, temperature, humidity, pressure])

# write the data to a CSV file
with open("weather_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("weather_data.csv")

# Create the Choropleth map
fig = px.choropleth(df, locations='State Codes', color='Temperature', title="Average Temperature by US State",
                    color_continuous_scale="Viridis", range_color=(0, 100))

# Show the map
fig.show()