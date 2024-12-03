"""
    Name: nws_cli.py
    Author:
    Created:
    Purpose: OOP console app
    Get weather data from the National Weather Service
"""
from time import sleep
import os
# Control textwrapping in the console
import textwrap
from datetime import datetime
# Windows: pip install rich
# Import Console for console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
from rich.table import Table

import nws_class
# Import geocode_geopy module for reverse geocode
import geocode_geopy

# Initialize rich.console
console = Console(highlight=False)
# os.system call to clear the console for Windows 'cls' or Linux 'clear'


class NWSConsole():
    def __init__(self) -> None:
        self.clear_console()
        console.print(Panel.fit(
            "    National Weather Service App    ",
            style="bold blue",
            subtitle="By William Loring"
        ))
        # Create weather object to access methods
        self.weather = nws_class.WeatherClass()

# ----------------------- GET LOCATION ----------------------------------- #
    def get_location(self):
        """Get lat, lng, and address to retrieve gridpoint for weather"""
        try:
            # Get location input from user
            city = input(" Enter city: ")
            state = input(" Enter state: ")

            # Get location lat, lng, and address from geopy
            # NWS is US only
            self.lat, self.lng, self.address = geocode_geopy.geocode(
                city, state, country="")
            print(f" {self.address}")
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)
            self.get_location()

        self.weather.get_gridpoints(self.lat, self.lng)

# -------------------- DISPLAY MENU -------------------------------------- #
    def get_menu_choice(self):
        """Print menu for user, return menu choice"""
        console.print("[green] (1)[/] Latest weather observation")
        console.print("[green] (2)[/] 12 hour forecast")
        console.print("[green] (3)[/] 7 day forecast")
        console.print("[green] (4)[/] 7 day detailed forecast")
        console.print("[green] (5)[/] Active weather alerts")
        console.print("[green] (6)[/] Weather alerts")
        console.print("[green] (9)[/] New location")
        console.print(
            "[green] [Enter][/] to quit. Enter your choice: ", end="")
        menu_choice = input()
        return menu_choice

# --------------- DISPLAY LATEST WEATHER OBSERVATION -----------------------#
    def display_latest_weather_observation(self):
        """Display latest weather observation from
            closest station in Rich table format
        """
        msg = f"National Weather Service - Latest Observations"
        msg += f"\n{self.address}\n{self.weather.station_name}"
        console.print(Panel.fit(
            msg,
            style="bold blue"
        ))
        table = Table(show_lines=True)
        table.add_column("Desc", justify="right")
        table.add_column("Value")
        table.add_column("Desc", justify="right")
        table.add_column("Value")
        table.add_row(f"{self.weather.description}")
        table.add_row(
            "Temperature ", f"{self.weather.temperature}°F",
            "Pressure", f"{self.weather.pressure} inHg"
        )
        table.add_row("Dew Point", f"{self.weather.dewpoint}°F",
                      "Visibility", f"{self.weather.visibility} mi")
        table.add_row("Humidity", f"{self.weather.humidity}%",
                      "Wind Chill",  f"{self.weather.windchill}°F")
        table.add_row(
            "Wind Direction",  f"{self.weather.degree}°  {
                self.weather.wind_cardinal}",
            "Heat Index", f"{self.weather.heatindex}°F")
        table.add_row(
            "Wind Speed", f"{self.weather.wind_speed} mph",
            "Elevation", f"{self.weather.elevation} feet")

        console.print(table)

# -------------------- DISPLAY 12 HOUR FORECAST -------------------------- #
    def display_twelve_hour_forecast(self):
        """Display 12 hour forecast"""
        msg = f"National Weather Service - 12 Hour Forecast"
        msg += f"n{self.address}\n{self.weather.station_name}"
        console.print(Panel.fit(
            msg,
            style="bold blue"
        ))

        try:
            # Slice 12 hours out of the hourly forecast list
            hourly_slice = self.weather.forecast_hourly_list[:12]

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
                    f" {time:>8}: {temperature:>5.1f}°F | {wind_speed:>8} | {
                        wind_direction:>5} | {short_forecast}"
                )

        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)

# ---------------------- DISPLAY 7 DAY FORECAST ----------------------------#
    def display_7_day_forecast(self):
        """Display 7 day forecast"""
        console.print(Panel.fit(
            f"National Weather Service - 7 Day Forecast\n{self.address}\n{self.weather.station_name}"),
            style="bold blue"
        )

        try:
            # Iterate through each item in the forecast list
            for forecast_item in self.weather.forecast_list:
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
                    f" {name:<15} {temperature:>4}°F | {wind_speed:12} {
                        wind_direction:5} | {short_forecast}"
                )
                # print(f'{detailed_forecast}')
        except Exception as e:
            print("Something went wrong. Let's try again")
            print(e)

# ----------------- DISPLAY 7 DAY DETAILED FORECAST ------------------------#
    def display_7_day_detailed_forecast(self):

        msg = f"National Weather Service - 7 Day Detailed Forecast"
        msg += f"\n{self.address}\n{self.weather.station_name}"
        console.print(Panel.fit(
            msg,
            style="bold blue"
        ))

        counter = 0
        # Iterate through each item in the forecast list
        for forecast_item in self.weather.forecast_list:
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

# ------------------- DISPLAY ACTIVE WEATHER ALERTS ------------------------#
    def display_active_weather_alerts(self):
        """Display active weather alerts"""

        msg = f"National Weather Service - Active Weather Alerts"
        msg += f"\n{self.address}\n{self.weather.station_name}"
        console.print(Panel.fit(
            msg,
            style="bold blue"
        ))

        # print(self.alert_dict.get("features")[0].get("properties").get("areaDesc"))
        active_alert_list = self.weather.active_weather_alert_dict.get("features")[
            :]

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

# ---------------------- DISPLAY WEATHER ALERTS ----------------------------#
    def display_weather_alerts(self):
        """Display weather alerts"""
        console.print(Panel.fit(
            f"National Weather Service Weather\
                 Alerts\n{self.address}\n{self.weather.station_name}",
            style="bold blue"
        ))

        # print(self.alert_dict.get("features")[0].get("properties").get("areaDesc"))
        alert_list = self.weather.weather_alert_dict.get("features")[:]

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

# -------------------------- MENU PROGRAM ----------------------------------#
    def menu(self):
        # Get the location from the user
        self.get_location()
        # Menu loop
        while True:
            # Get menu choice
            menu_choice = self.get_menu_choice()

            # If the user presses the enter key, exit program
            if menu_choice == "":
                # Exit loop
                break

            # Display latest weather observations
            elif menu_choice == "1":
                self.clear_console()
                self.weather.get_latest_weather_observation()
                self.weather.process_latest_weather_observation()
                self.display_latest_weather_observation()

            # Get 12 hour forecast
            elif menu_choice == "2":
                self.clear_console()
                self.weather.get_hourly_forecast()
                self.display_twelve_hour_forecast()

            # Get 7 day forecast
            elif menu_choice == "3":
                self.clear_console()
                self.weather.get_7_day_forecast()
                self.display_7_day_forecast()

            # Get and display 7 day detailed forecast
            elif menu_choice == "4":
                self.clear_console()
                self.weather.get_7_day_forecast()
                self.display_7_day_detailed_forecast()

            # Get and display active weather alerts
            elif menu_choice == "5":
                self.clear_console()
                self.weather.get_active_weather_alerts(self.lat, self.lng)
                self.display_active_weather_alerts()

            # Get and display weather alerts
            elif menu_choice == "6":
                self.clear_console()
                self.weather.get_weather_alerts(self.lat, self.lng)
                self.display_weather_alerts()

            # Make API call for a new location
            elif menu_choice == "9":
                self.clear_console()
                self.get_location()

        # Say goodbye to the user as the program exits
        self.goodbye()

# -------------------------- CLEAR CONSOLE ---------------------------------#
    def clear_console(self):
        # Clear the console for Windows 'cls' or Linux 'clear'
        os.system("cls" if os.name == "nt" else "clear")

# ----------------------------- GOODBYE ------------------------------------#
    def goodbye(self):
        """Print goodbye to user"""
        console.print(Panel.fit(
            "    Good bye from Bill's NWS Weather App!    ",
            style="bold blue"
        ))
        sleep(2)


# Create program object to start program
nws_console = NWSConsole()
nws_console.menu()
