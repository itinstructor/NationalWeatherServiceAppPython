import requests

# Latitude and longitude of Scottsbluff, NE
latitude = 41.89
longitude = -103.67

# NWS API endpoint
points_url = f"https://api.weather.gov/points/{latitude},{longitude}"

# Fetch location information
response = requests.get(points_url)
data = response.json()
# print(data)
# Extract observation station URL
observation_stations_url = data['properties']['observationStations']

# Fetch observation station data
stations_response = requests.get(observation_stations_url)
stations_data = stations_response.json()
stations = stations_data['observationStations']

# Fetch data from the first observation station
station_url = stations[0]

# Fetch current weather data
current_weather_url = f"{station_url}/observations/latest"
current_weather_response = requests.get(current_weather_url)
current_weather_data = current_weather_response.json()
# print(current_weather_data)

# Print current weather information
current_observation = current_weather_data['properties']

temp_c = current_observation['temperature']['value']
temp_f = temp_c * (9.0 / 5.0) + 32

print("Current Weather")
print(f"Temperature: {temp_f} °F")
print(f"Humidity: {current_observation['relativeHumidity']['value']}%")
print(f"Wind Speed: {current_observation['windSpeed']['value']} m/s")
print(f"Wind Direction: {current_observation['windDirection']['value']}°")
print(f"Weather Description: {current_observation['textDescription']}")
