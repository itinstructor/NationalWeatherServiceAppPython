"""
    Name: nws_class.py
    Author:
    Revised: 07/17/22
    Purpose: OOP class for National Weather Service weather
    Get lat and lon from geocode
    Separate out API calls into separate methods.
"""

import requests
# Control textwrapping in the console
import textwrap
# os.system call to clear the console for Windows 'cls' or Linux 'clear'
import os
import weather_utils
# Import geocode_geopy module for reverse geocode
import geocode_geopy
from datetime import datetime
from time import sleep
# Windows: pip install rich
# Import Console for console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
from rich.table import Table

# Initialize rich.console
console = Console()


class WeatherClass:
    def __init__(self):
        """ Initialize object """
        self.clear_console()
        console.print(Panel.fit(
            "    National Weather Service App    ",
            style="bold blue",
            subtitle="By William Loring"
        ))
        self._decorator_width = 75

        # User agent headers dictionary, like an API key, Required by NWS
        self.headers = {
            "User-Agent": "(nws_app, williamloring@hotmail.com)"
        }

#--------------------------------- GET LOCATION -------------------------------------#
    def get_location(self):
        """
            Get lat, lng, and address to retrieve gridpoint for weather
        """
        try:
            # Get location input from user
            city = input(" Enter city: ")
            state = input(" Enter state: ")

            # Get location lat, lng and address from geopy
            # NWS is US only
            self.lat, self.lng, self._address = geocode_geopy.geocode(
                city, state, country="")
            print(f" {self._address}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception
        self.get_gridpoints()

#--------------------------------- GET GRIDPOINTs -------------------------------------#
    def get_gridpoints(self):
        """
            Gridpoints are how the NWS locates the weather
            lat, lng are translated into gridpoints
            gridpoints allow us to get the weather for the current location
        """
        try:
            # Create url from lat and lng to get gridpoints
            points_url = weather_utils.NWS_ENDPOINT + "/points/" + \
                str(self.lat) + "," + str(self.lng)

            # Get the gridpoints response
            response = requests.get(points_url, headers=self.headers)

            # Get gridpoints dictionary, locations for weather station coverage
            if(response.status_code == 200):
                print(
                    " [+] The connection to the National Weather Service was successful.")
                # Get the gridpoints dictionary for weather station locations
                self.grid_points_dict = response.json()
                print(
                    f" [+] Retrieved NWS Gridpoints for Weather Station Location")

            else:
                print("[-] Did not get NWS Gridpoints")

        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#--------------------------------- GET LATEST WEATHER OBSERVATION -------------------------------------#
    def get_latest_weather_observation(self):
        """
            Get latest weather observation from closest station
        """
        try:
            # Get closest observation station URL from grid_points dictionary
            stations_url = self.grid_points_dict.get(
                "properties").get("observationStations")
            response = requests.get(stations_url, headers=self.headers)

            # Get observation station ids
            if(response.status_code == 200):
                # Get station dictionary
                self.station_dict = response.json()

                # Get first station id in list
                self.station_id = self.station_dict.get("features")[0].get(
                    "properties").get("stationIdentifier")

                # Create URL from station id
                observations_url = weather_utils.NWS_ENDPOINT + \
                    "stations/" + self.station_id + "/observations/latest"
                response = requests.get(observations_url, headers=self.headers)
            else:
                print(
                    f"[-] Did not get Station ID - - Response: {response.status_code}")

            # Get latest observation from station
            if(response.status_code == 200):
                # Get latest observation dictionary
                self.weather_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS latest weather observation \
                        - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

 #------------------------------------- GET HOURLY FORECAST ----------------------------------------#
    def get_hourly_forecast(self):
        """
           Get hourly forecast url from grid_points dictionary
        """
        try:
            forecast_hourly_url = self.grid_points_dict.get(
                "properties").get("forecastHourly")
            response = requests.get(forecast_hourly_url, headers=self.headers)

            if(response.status_code == 200):
                # Get forecast dictionary
                forecast_hourly_dict = response.json()
                self.forecast_hourly_list = forecast_hourly_dict.get(
                    "properties").get("periods")
            else:
                print(
                    f"[-] Did not get NWS Hourly Forecast - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#--------------------------------- GET 7 DAY FORECAST -------------------------------------#
    def get_7_day_forecast(self):
        """
            Get 7 Day forecast from grid_points dictionary
        """
        try:
            # Get the forecast url from the gridpoints dictionary
            forecast_url = self.grid_points_dict.get(
                "properties").get("forecast")

            response = requests.get(forecast_url, headers=self.headers)

            if(response.status_code == 200):
                # Get forecast dictionary
                forecast_dict = response.json()
                self.forecast_list = forecast_dict.get(
                    "properties").get("periods")
            else:
                print(
                    f"[-] Did not get NWS 7 Day Forecast - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#--------------------------------- GET ACTIVE WEATHER ALERTS ----------------------------#
    def get_active_weather_alerts(self):
        """
            Get active weather alerts for the area
        """
        try:
            active_alerts_url = f"https://api.weather.gov/alerts/active?point={self.lat},{self.lng}"
            response = requests.get(active_alerts_url, headers=self.headers)
            if(response.status_code == 200):
                self.active_weather_alert_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS Active Weather Alerts - Response: {response.status_code}")

        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#--------------------------------- GET WEATHER ALERTS ----------------------------#
    def get_weather_alerts(self):
        """
            Get weather alerts for the area
        """
        try:
            alerts_url = f"https://api.weather.gov/alerts?point={self.lat},{self.lng}"
            response = requests.get(alerts_url, headers=self.headers)
            if(response.status_code == 200):
                self.weather_alert_dict = response.json()
            else:
                print(
                    f"[-] Did not get NWS Weather Alerts - Response: {response.status_code}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#-------------------------- DISPLAY ACTIVE WEATHER ALERTS ----------------------------#
    def display_active_weather_alerts(self):
        """
            Display active weather alerts
        """
        console.print(Panel.fit(
            f"National Weather Service Active Weather Alerts\n{self._address}\n{self.station_name}",
            style="bold blue"
        ))

        # print(self.alert_dict.get("features")[0].get("properties").get("areaDesc"))
        active_alert_list = self.active_weather_alert_dict.get("features")[:]

        # If active weather alert list is not empty
        if active_alert_list != []:
            for alert in active_alert_list:
                area = alert.get("properties").get("areaDesc")
                headline = alert.get("properties").get("headline")
                description = alert.get("properties").get("description")

                effective = alert.get("properties").get("effective")
                effective = datetime.fromisoformat(effective)
                effective = effective.strftime(
                    "%m/%d/%Y, %I:%M %p")  # , %-I:%M %p

                expires = alert.get("properties").get("expires")
                expires = datetime.fromisoformat(expires)
                expires = expires.strftime("%m/%d/%Y, %I:%M %p")  # , %-I:%M %p

                wrapper = textwrap.TextWrapper(width=70)
                area = wrapper.fill(text=area)
                headline = wrapper.fill(text=headline)
                description = wrapper.fill(text=description)

                print("*" * 70)
                print(f"Effective: {effective}")
                print(f"Expires: {expires}")
                print(f"{area}")
                print(f"{headline}")
                print(f"{description}")
                input("Press the enter key for the next alert")
        else:
            print("No active weather alerts at this time.")

#-------------------------- DISPLAY WEATHER ALERTS ----------------------------#
    def display_weather_alerts(self):
        """
            Display weather alerts
        """
        console.print(Panel.fit(
            f"National Weather Service Weather Alerts\n{self._address}\n{self.station_name}",
            style="bold blue"
        ))

        # print(self.alert_dict.get("features")[0].get("properties").get("areaDesc"))
        alert_list = self.weather_alert_dict.get("features")[:]

        # If weather alert list is not empty
        if alert_list != []:
            for alert in alert_list:
                area = alert.get("properties").get("areaDesc")
                headline = alert.get("properties").get("headline")
                description = alert.get("properties").get("description")

                effective = alert.get("properties").get("effective")
                effective = datetime.fromisoformat(effective)
                effective = effective.strftime(
                    "%m/%d/%Y, %I:%M %p")  # , %-I:%M %p

                expires = alert.get("properties").get("expires")
                expires = datetime.fromisoformat(expires)
                expires = expires.strftime("%m/%d/%Y, %I:%M %p")  # , %-I:%M %p

                wrapper = textwrap.TextWrapper(width=70)
                area = wrapper.fill(text=area)
                headline = wrapper.fill(text=headline)
                description = wrapper.fill(text=description)

                print("*" * 70)
                print(f"Effective: {effective}")
                print(f"Expires: {expires}")
                print(f"{area}")
                print(f"{headline}")
                print(f"{description}")
                input("Press the enter key for the next alert")
        else:
            print("No weather alerts at this time.")

#-------------------------- PROCESS LATEST WEATHER OBSERVATION ----------------------------#
    def process_latest_weather_observation(self):
        """
            Get latest observation from the closest NWS station
        """
        # Get nearest stationid
        self.station_name = self.station_dict.get(
            "features")[0].get("properties").get("name")

        # Get latest weather observation from dictionary
        # Shorten up weather observations dictionary code
        weather_obs = self.weather_dict.get("properties")

        timestamp = weather_obs.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp)
        self._timestamp = timestamp.strftime("%m/%d/%Y, %I:%M %p")

        description = weather_obs.get("textDescription")
        if not (description is None):
            self._description = description
        else:
            self._description = "NA"

        temperature = weather_obs.get("temperature").get("value")
        if not (temperature is None):
            self._temperature = weather_utils.celsius_to_fahrenheit(
                temperature)
        else:
            self._temperature = "NA"

        dewpoint = weather_obs.get("dewpoint").get("value")
        if not (dewpoint is None):
            self._dewpoint = round(dewpoint, 1)
        else:
            self._dewpoint = "NA"

        humidity = weather_obs.get("relativeHumidity").get("value")
        if not (humidity is None):
            self._humidity = round(humidity)
        else:
            self._humidity = "NA"

        wind_speed = weather_obs.get("windSpeed").get("value")
        if not (wind_speed is None):
            # Convert kph to mph
            self._wind_speed = round(wind_speed * .621371, 1)
        else:
            self._wind_speed = "NA"

        wind_direction = weather_obs.get("windDirection").get("value")
        if not (wind_direction is None):
            # Convert kph to mph
            self._degree = wind_direction
            self._wind_cardinal = weather_utils.degrees_to_cardinal(
                wind_direction)
        else:
            self._degree = "NA"
            self._wind_cardinal = "NA"

        pressure = weather_obs.get("barometricPressure").get("value")
        if not (pressure is None):
            # Convert pascals to inches of mercury inHg
            self._pressure = round(pressure / 3386, 2)
        else:
            self._pressure = "NA"

        visibility = weather_obs.get("visibility").get("value")
        if not (visibility is None):
            self._visibility = round((visibility * 3.28084) / 5280)
        else:
            self._visibility = "NA"

        windchill = weather_obs.get("windChill").get("value")
        if not (windchill is None):
            # Convert meters to miles
            self._windchill = weather_utils.celsius_to_fahrenheit(windchill)
        else:
            self._windchill = "NA"

        heatindex = weather_obs.get("visibility").get("value")
        if not (pressure is None):
            # Convert meters to miles
            self._heatindex = round(heatindex * 0.000621371)
        else:
            self._heatindex = "NA"

        elevation = weather_obs.get("elevation").get("value")
        if not (elevation is None):
            # Convert meters to miles
            self._elevation = round(elevation * 3.28084)
        else:
            self._elevation = "NA"

#-------------------------- DISPLAY LATEST WEATHER OBSERVATION ----------------------------#
    def display_latest_weather_observation(self):
        """
            Display latest weather observation from closest station in Rich table format
        """
        console.print(Panel.fit(
            f"National Weather Service Latest Observations\n{self._address}\n{self.station_name}",
            style="bold blue"
        ))
        table = Table()
        table.add_column("Desc", justify="right")
        table.add_column("Value")
        table.add_column("Desc", justify="right")
        table.add_column("Value")
        table.add_row(f"{self._description}", "")
        table.add_row(
            "Temperature ", f"{self._temperature}°F", "Pressure", f"{self._pressure} inHg")
        table.add_row("Dew Point", f"{self._dewpoint}°F",
                      "Visibility", f"{self._visibility} mi")
        table.add_row("Humidity", f"{self._humidity}%",
                      "Wind Chill",  f"{self._windchill}°F")
        table.add_row(
            "Wind Direction",  f"{self._degree}°  {self._wind_cardinal}", "Heat Index", f"{self._heatindex}°F")
        table.add_row(
            "Wind Speed", f"{self._wind_speed} mph", "Elevation", f"{self._elevation} feet")

        console.print(table)

#-------------------------- DISPLAY 12 HOUR FORECAST ----------------------------#
    def display_twelve_hour_forecast(self):
        """
            Display 12 hour forecast
        """
        console.print(Panel.fit(
            f"National Weather Service 12 Hour Forecast\n{self._address}\n{self.station_name}",
            style="bold blue"
        ))

        try:
            # Slice 12 hours out of the hourly forecast list
            hourly_slice = self.forecast_hourly_list[:12]
            # Iterate through each item in the forecast list
            for forecast_item in hourly_slice:
                start_time = forecast_item.get("startTime")
                temperature = forecast_item.get("temperature")
                wind_speed = forecast_item.get("windSpeed")
                wind_direction = forecast_item.get("windDirection")
                short_forecast = forecast_item.get("shortForecast")
                time = datetime.fromisoformat(start_time)
                time = time.strftime('%I:%M %p')
                print(
                    f" {time:>8}: {temperature:>5.1f}°F | {wind_speed:>8} | {wind_direction:>5} | {short_forecast}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#-------------------------- DISPLAY 7 DAY FORECAST ----------------------------#
    def display_7_day_forecast(self):
        """
            Display 7 day forecast
        """
        console.print(Panel.fit(
            f"National Weather Service 7 Day Forecast\n{self._address}\n{self.station_name}"),
            style="bold blue"
        )

        try:
            # Iterate through each item in the forecast list
            for forecast_item in self.forecast_list:
                # start_time = forecast_item.get("startTime")
                name = forecast_item.get("name")
                temperature = forecast_item.get("temperature")
                wind_speed = forecast_item.get("windSpeed")
                wind_direction = forecast_item.get("windDirection")
                short_forecast = forecast_item.get("shortForecast")
                # detailed_forecast = forecast_item.get("detailedForecast")
                # time = datetime.fromisoformat(start_time)
                # time = time.strftime('%m-%d-%Y')
                # print(f"{name}: {detailed_forecast}")
                print(
                    f" {name:<15} {temperature:>4}°F | {wind_speed:12} {wind_direction:5} | {short_forecast}")
                # print(f'{detailed_forecast}')
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            # raise exception is used to troubleshoot
            # It raises the exception that was handled
            # raise exception

#-------------------------- DISPLAY 7 DAY DETAILED FORECAST ----------------------------#
    def display_7_day_detailed_forecast(self):

        console.print(Panel.fit(
            f"National Weather Service 7 Day Detailed Forecast\n{self._address}\n{self.station_name}",
            style="bold blue"
        ))

        counter = 0
        # Iterate through each item in the forecast list
        for forecast_item in self.forecast_list:
            # start_time = forecast_item.get("startTime")
            name = forecast_item.get("name")
            # temperature = forecast_item.get("temperature")
            # wind_speed = forecast_item.get("windSpeed")
            # wind_direction = forecast_item.get("windDirection")
            # short_forecast = forecast_item.get("shortForecast")
            detailed_forecast = forecast_item.get("detailedForecast")
            wrapper = textwrap.TextWrapper(width=60)
            detailed_forecast = wrapper.fill(text=detailed_forecast)
            # time = datetime.fromisoformat(start_time)
            # time = time.strftime('%m-%d-%Y')
            print(f" {name}: \n{detailed_forecast}\n")
            # print(f"{temperature} °F | {wind_speed:5} {wind_direction}")
            # print(f'{detailed_forecast}')
            counter += 1
            if (counter % 4 == 0):
                input(" Press Enter for More")
                self.clear_console()
                # print("="*self.__decorator_width)

#--------------------------------- GOODBYE --------------------------------#
    def goodbye(self):
        """
            Print goodbye to user
        """
        console.print(Panel.fit(
            "    Good bye from Bill's NWS Weather App!    ",
            style="bold blue"
        ))
        sleep(2)

#-------------------------- CLEAR CONSOLE ----------------------------#
    def clear_console(self):
        # Clear the console for Windows 'cls' or Linux 'clear'
        os.system("cls" if os.name == "nt" else "clear")
