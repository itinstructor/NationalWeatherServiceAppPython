import requests
import pandas as pd
import matplotlib.pyplot as plt

# Latitude and longitude of Scottsbluff, NE
latitude = 41.89
longitude = -103.67

# NWS API endpoint
points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
response = requests.get(points_url)
data = response.json()

# Extract forecast URL
forecast_url = data['properties']['forecast']

# Fetch forecast data
forecast_response = requests.get(forecast_url)
forecast_data = forecast_response.json()

# Extract high/low temperature data by date
periods = forecast_data['properties']['periods']
dates = [period['startTime'][:10] for period in periods if period['isDaytime']]
highs = [period['temperature'] for period in periods if period['isDaytime']]
lows = [period['temperature'] for period in periods if not period['isDaytime']]

# Create a DataFrame
df = pd.DataFrame({
    'Date': dates[:len(lows)],
    'High': highs[:len(lows)],
    'Low': lows
})

# Visualize the data
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['High'], label='High Temp (F)', marker='o')
plt.plot(df['Date'], df['Low'], label='Low Temp (F)', marker='o')
plt.fill_between(df['Date'], df['High'], df['Low'], color='grey', alpha=0.2)
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.title('7-Day Temperature Forecast for Dallas, TX')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()