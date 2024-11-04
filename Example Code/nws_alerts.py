import requests

# Latitude and longitude of Scottsbluff, NE
latitude = 41.89
longitude = -103.67

# NWS API endpoint
points_url = f"https://api.weather.gov/points/{latitude},{longitude}"

# Fetch location information
response = requests.get(points_url)
data = response.json()

# Extract alert URL
forecast_zone_url = data['properties']['forecastZone']

# Fetch alert data
alerts_url = f"https://api.weather.gov/alerts/active?zone={forecast_zone_url.split('/')[-1]}"
alerts_response = requests.get(alerts_url)
alerts_data = alerts_response.json()

# Print alert information
alerts = alerts_data['features']

if alerts:
    print("Current Weather Alerts and Notifications")
    for alert in alerts:
        properties = alert['properties']
        print(f"Title: {properties['headline']}")
        print(f"Event: {properties['event']}")
        print(f"Description: {properties['description']}")
        print(f"Instructions: {properties['instruction']}")
        print("-" * 40)
else:
    print("There are no active weather alerts and notifications.")