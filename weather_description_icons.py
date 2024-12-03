"""According to the "api.weather.gov" documentation, the "textDescription"
 field can contain a variety of descriptive phrases regarding the 
 current weather conditions, including:
   "Mostly Sunny," "Partly Cloudy," "Cloudy," "Scattered Showers," "Thunderstorms," "Rain," "Snow," "Freezing Rain," "Fog," "Mist," "Haze," "Blowing Snow," "Snow Showers," "Ice Pellets," "Drizzle," "Squalls," "Windy," "High Wind," "Cold," "Hot," "Dry," and "Humid"; essentially providing a human-readable summary of the weather type. """

# Comprehensive list of possible text descriptions from api.weather.gov
WEATHER_DESCRIPTIONS = [
    # Clear/Sunny Conditions
    "Sunny", "Clear", "Mostly Clear", "Partly Cloudy",

    # Cloud Conditions
    "Mostly Cloudy", "Overcast", "Cloudy",

    # Precipitation Types
    "Rain", "Light Rain", "Heavy Rain", "Scattered Rain",
    "Drizzle", "Light Drizzle", "Heavy Drizzle",
    "Freezing Rain", "Sleet", "Snow", "Light Snow", "Heavy Snow",
    "Scattered Snow", "Flurries", "Blowing Snow",
    "Thunderstorms", "Scattered Thunderstorms", "Severe Thunderstorms",
    "Thunderstorm in Vicinity", "Rain Showers", "Snow Showers",

    # Fog and Mist
    "Fog", "Dense Fog", "Mist", "Haze", "Smoke",

    # Wind Conditions
    "Windy", "Breezy", "Gusts",

    # Mixed Conditions
    "Partly Sunny", "Mostly Sunny",
    "Rain and Snow", "Sleet and Rain",

    # Severe Weather
    "Tornado Warning", "Hurricane Warning", "Severe Thunderstorm Warning",
    "Dust Storm", "Sandstorm",

    # Temperature-Related
    "Freezing Conditions", "Frost", "Ice",

    # Night Conditions
    "Mostly Clear", "Partly Cloudy", "Mostly Cloudy",

    # Seasonal/Regional
    "Blowing Sand", "Blowing Dust", "Volcanic Ash"
]
