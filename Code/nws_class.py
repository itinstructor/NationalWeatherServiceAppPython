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
        EMAIL_ADDRESS = "your email address"
        # User agent headers dictionary, like an API key, Required by NWS
        self.headers = {
            "User-Agent": f"(nws_app, {EMAIL_ADDRESS})"
        }

#--------------------- GET GRIDPOINTS FROM LAT LON-----------------------------#
    def get_gridpoints(self, lat, lng):
        """
            Gridpoints are how the NWS locates the weather
            lat, lng are translated into gridpoints
            gridpoints allow us to get the weather for the current location
        """
        try:
            # Create url from lat and lng to get gridpoints
            points_url = weather_utils.NWS_ENDPOINT + "/points/" + \
                str(lat) + "," + str(lng)

            # Get the gridpoints response
            response = requests.get(points_url, headers=self.headers)

            # Get gridpoints dictionary, locations for weather station coverage
            if (response.status_code == 200):
                print(
                    " [+] Connection to the National Weather Service was successful.")
                # Get the gridpoints dictionary for weather station locations
                self.grid_points_dict = response.json()
                print(
                    f" [+] Retrieved NWS Gridpoints for Station Location")
            else:
                print("[-] Did not get NWS Gridpoints")

        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception
        self.get_station_name()

#--------------------------- GET STATION NAME ---------------------------------#
    def get_station_name(self):
        """
            Get station name
        """
        try:
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
                print(
                    f"[-] Did not get station_id or station_name \
                        - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#------------------ GET LATEST WEATHER OBSERVATION ----------------------------#
    def get_latest_weather_observation(self):
        """
            Get latest weather observation from closest station
        """
        try:
            # Create URL from station id
            observations_url = weather_utils.NWS_ENDPOINT + \
                "stations/" + self.station_id + "/observations/latest"
            response = requests.get(observations_url, headers=self.headers)

            # Get latest observation from station
            if (response.status_code == 200):
                # Get latest observation dictionary
                self.weather_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS latest weather observation \
                        - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

 #----------------------- GET HOURLY FORECAST ---------------------------------#
    def get_hourly_forecast(self):
        """
           Get hourly forecast url from grid_points dictionary
        """
        try:
            forecast_hourly_url = self.grid_points_dict.get(
                "properties").get("forecastHourly")
            response = requests.get(
                forecast_hourly_url, headers=self.headers, timeout=3)

            if (response.status_code == 200):
                # Get forecast dictionary
                forecast_hourly_dict = response.json()
                self.forecast_hourly_list = forecast_hourly_dict.get(
                    "properties").get("periods")
            else:
                print(
                    f"[-] Did not get NWS Hourly Forecast\
                        - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#----------------------- GET 7 DAY FORECAST -----------------------------------#
    def get_7_day_forecast(self):
        """
            Get 7 Day forecast from grid_points dictionary
        """
        try:
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
                print(
                    f"[-] Did not get NWS 7 Day Forecast\
                         - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#----------------------- GET ACTIVE WEATHER ALERTS ----------------------------#
    def get_active_weather_alerts(self, lat, lng):
        """
            Get active weather alerts for the area
        """
        try:
            active_alerts_url = f"https://api.weather.gov/alerts/active?point={lat},{lng}"
            response = requests.get(active_alerts_url, headers=self.headers)
            if (response.status_code == 200):
                self.active_weather_alert_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS Active Weather Alerts\
                         - Response: {response.status_code}")

        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#------------------------------ GET WEATHER ALERTS ----------------------------#
    def get_weather_alerts(self, lat, lng):
        """
            Get weather alerts for the area
        """
        try:
            alerts_url = f"https://api.weather.gov/alerts?point={lat},{lng}"
            response = requests.get(alerts_url, headers=self.headers)
            if (response.status_code == 200):
                self.weather_alert_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS Weather Alerts\
                         - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#------------------ PROCESS LATEST WEATHER OBSERVATION ------------------------#
    def process_latest_weather_observation(self):
        """
            Get latest observation from the closest NWS station
        """
        # Get nearest station name
        # self.station_name = self.station_dict.get(
        #     "features")[0].get("properties").get("name")

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
            self.pressure = round(pressure / 3386, 2)
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
