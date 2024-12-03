"""
    Name: nws_class.py
    Author:
    Revised: 07/17/22
    Purpose: OOP class for National Weather Service weather
    Separate out API calls into separate methods
"""

import requests
import weather_utils
from datetime import datetime


class WeatherClass:
    def __init__(self):
        # Replace with your email address
        EMAIL_ADDRESS = "youremailaddress@your.com"

        # User agent headers dictionary, like an API key, Required by NWS
        self.headers = {
            "User-Agent": f"(nws_app, {EMAIL_ADDRESS})"
        }

# ----------------- GET GRIDPOINTS FROM LAT LON -------------------------- #
    def get_gridpoints(self, lat, lng):
        """Retrieves the gridpoints for the given latitude and longitude 
        from the National Weather Service (NWS).
        Gridpoints are used by the NWS to locate 
        weather information for a specific location.
        Args:
            lat (float): The latitude of the location.
            lng (float): The longitude of the location.
        Returns:
            str: An error message if the gridpoints could not be retrieved.
        """
        # Create url from lat and lng to get gridpoints
        points_url = weather_utils.NWS_ENDPOINT + "/points/" + \
            str(lat) + "," + str(lng)

        # Get the gridpoints response
        response = requests.get(points_url, headers=self.headers)

        # Get gridpoints dictionary, locations for weather station coverage
        if (response.status_code == 200):
            # Get the gridpoints dictionary for weather station locations
            self.grid_points_dict = response.json()

        else:
            return "[-] Did not get NWS Gridpoints"

        self.get_station_name()

# ----------------------- GET STATION NAME ------------------------------- #
    def get_station_name(self):
        """
        Retrieves the name of the nearest weather observation station.
        This method fetches the URL of the closest observation station from the 
        grid_points dictionary, sends a GET request to that URL, and extracts the 
        station ID and name from the response. If the request is successful, the 
        station ID and name are stored in the instance variables `station_id` and 
        `station_name`, respectively. If the request fails, an error message with 
        the response status code is returned.
        Returns:
            str: An error message if the request fails, otherwise None.
        """
        
        # Get closest observation station URL from grid_points dictionary
        stations_url = self.grid_points_dict.get(
            "properties").get("observationStations")

        response = requests.get(stations_url, headers=self.headers)

        # Get observation station ids
        if (response.status_code == 200):
            # Get station dictionary
            self.station_dict = response.json()

            # Get first station id in list
            self.station_id = self.station_dict.get("features")[0].get(
                "properties").get("stationIdentifier")

            # Get nearest station name
            self.station_name = self.station_dict.get(
                "features")[0].get("properties").get("name")
        else:
            return f"[-] Did not get station_id or station_name \
                    - Response: {response.status_code}"

# -------------- GET LATEST WEATHER OBSERVATION -------------------------- #
    def get_latest_weather_observation(self):
        """
        Fetches the latest weather observation from the 
        National Weather Service (NWS) for the specified station.
        This method constructs the URL using the station ID and sends a GET
        request to the NWS endpoint to retrieve the latest weather observation. 
        If the request is successful (status code 200), 
        it updates the weather dictionary with the response data. 
        Otherwise, it returns an error message with the response status code.
        Returns:
            str: An error message if the request fails, otherwise None.
        """
        
        # Create URL from station id
        observations_url = weather_utils.NWS_ENDPOINT + \
            "stations/" + self.station_id + "/observations/latest"

        response = requests.get(observations_url, headers=self.headers)

        # Get latest observation from station
        if (response.status_code == 200):
            # Get latest observation dictionary
            self.weather_dict = response.json()
        else:
            return f"[-] Did not get NWS latest weather observation \
                    - Response: {response.status_code}"

 # ------------------- GET HOURLY FORECAST ------------------------------- #
    def get_hourly_forecast(self):
        """
        Fetches the hourly weather forecast from the National Weather Service (NWS) API.
        This method retrieves the hourly forecast data using the URL provided in the 
        grid_points_dict attribute. It sends a GET request to the NWS API and, if successful, 
        parses the JSON response to extract the forecast periods, which are then stored in 
        the forecast_hourly_list attribute.
        Returns:
            str: An error message if the request to the NWS API fails, including the response 
            status code.
        """
        
        forecast_hourly_url = self.grid_points_dict.get(
            "properties").get("forecastHourly")

        response = requests.get(
            forecast_hourly_url, headers=self.headers)

        if (response.status_code == 200):
            # Get forecast dictionary
            forecast_hourly_dict = response.json()
            self.forecast_hourly_list = forecast_hourly_dict.get(
                "properties").get("periods")
        else:
            return f"[-] Did not get NWS Hourly Forecast\
                    - Response: {response.status_code}"

# ------------------- GET 7 DAY FORECAST --------------------------------- #
    def get_7_day_forecast(self):
        """
        Fetches the 7-day weather forecast from the National Weather Service (NWS).
        This method retrieves the forecast URL from the grid points dictionary,
        makes a GET request to the NWS API, and processes the response to extract
        the 7-day forecast data.
        Returns:
            str: An error message if the request fails.
        """
        
        # Get the forecast url from the gridpoints dictionary
        forecast_url = self.grid_points_dict.get(
            "properties").get("forecast")

        response = requests.get(forecast_url, headers=self.headers)

        if (response.status_code == 200):
            # Get forecast dictionary
            forecast_dict = response.json()
            self.forecast_list = forecast_dict.get(
                "properties").get("periods")
        else:
            return f"[-] Did not get NWS 7 Day Forecast\
                        - Response: {response.status_code}"

# ------------------- GET ACTIVE WEATHER ALERTS -------------------------- #
    def get_active_weather_alerts(self, lat, lng):
        """Get active weather alerts for the area"""
        active_alerts_url = f"https://api.weather.gov/alerts/active?point={
            lat},{lng}"

        response = requests.get(active_alerts_url, headers=self.headers)

        if (response.status_code == 200):
            self.active_weather_alert_dict = response.json()

        else:
            return f"[-] Did not get NWS Active Weather Alerts\
                        - Response: {response.status_code}"

# -------------------------- GET WEATHER ALERTS -------------------------- #
    def get_weather_alerts(self, lat, lng):
        """Get weather alerts for the area"""
        alerts_url = f"https://api.weather.gov/alerts?point={lat},{lng}"

        response = requests.get(alerts_url, headers=self.headers)
        if (response.status_code == 200):
            self.weather_alert_dict = response.json()
        else:
            return f"[-] Did not get NWS Weather Alerts\
                        - Response: {response.status_code}"

# -------------- PROCESS LATEST WEATHER OBSERVATION ---------------------- #
    def process_latest_weather_observation(self):
        """Get latest observation from the closest NWS station"""
        # Get nearest station name
        # self.station_name = self.station_dict.get(
        #     "features")[0].get("properties").get("name")
        try:
            # Get latest weather observation from dictionary
            # Shorten up weather observations dictionary code
            weather_obs = self.weather_dict.get("properties")

            timestamp = weather_obs.get("timestamp")
            timestamp = datetime.fromisoformat(timestamp)
            self._timestamp = timestamp.strftime("%m/%d/%Y, %I:%M %p")

            description = weather_obs.get("textDescription")
            if not (description is None):
                self.description = description
            else:
                self.description = "NA"

            temperature = weather_obs.get("temperature").get("value")
            if not (temperature is None):
                self.temperature = weather_utils.celsius_to_fahrenheit(
                    temperature)
            else:
                self.temperature = "NA"

            dewpoint = weather_obs.get("dewpoint").get("value")
            if not (dewpoint is None):
                self.dewpoint = round(dewpoint, 1)
            else:
                self.dewpoint = "NA"

            humidity = weather_obs.get("relativeHumidity").get("value")
            if not (humidity is None):
                self.humidity = round(humidity)
            else:
                self.humidity = "NA"

            wind_speed = weather_obs.get("windSpeed").get("value")
            if not (wind_speed is None):
                # Convert kph to mph
                self.wind_speed = round(wind_speed * .621371, 1)
            else:
                self.wind_speed = "NA"

            wind_direction = weather_obs.get("windDirection").get("value")
            if not (wind_direction is None):
                # Convert kph to mph
                self.degree = wind_direction
                self.wind_cardinal = weather_utils.degrees_to_cardinal(
                    wind_direction)
            else:
                self.degree = "NA"
                self.wind_cardinal = "NA"

            pressure = weather_obs.get("barometricPressure").get("value")
            if not (pressure is None):
                # Convert pascals to inches of mercury inHg
                pressure = pressure / 3386.3886666667
                self.pressure = f"{pressure:.2f}"
            else:
                self.pressure = "NA"

            visibility = weather_obs.get("visibility").get("value")
            if not (visibility is None):
                self.visibility = round((visibility * 3.28084) / 5280)
            else:
                self.visibility = "NA"

            windchill = weather_obs.get("windChill").get("value")
            if not (windchill is None):
                # Convert celsius to fahrenheit
                self.windchill = weather_utils.celsius_to_fahrenheit(windchill)
            else:
                self.windchill = "NA"

            heatindex = weather_obs.get("visibility").get("value")
            if not (pressure is None):
                # Convert meters to miles
                self.heatindex = round(heatindex * 0.000621371)
            else:
                self.heatindex = "NA"

            elevation = weather_obs.get("elevation").get("value")
            if not (elevation is None):
                # Convert meters to miles
                self.elevation = round(elevation * 3.28084)
            else:
                self.elevation = "NA"

            # icon is deprecated
            # icon = weather_obs.get("icon")
            # if not (icon is None):
            #     # Convert meters to miles
            #     self.icon = icon
            # else:
            #     self.icon = "NA"

        except Exception as e:
            return f"[-] Error processing latest weather observation: {e}"
