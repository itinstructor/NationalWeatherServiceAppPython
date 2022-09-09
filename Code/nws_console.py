"""
    Name: nws_console.py
    Author:
    Created:
    Purpose: OOP console app
    Get weather data from the National Weather Service
"""
# Openweather map url, api key, and other weather utilities
import nws_class
# Windows: pip install rich
# Linux: pip3 install rich
# Import Console for console printing
from rich.console import Console

# Initialize rich.console
console = Console(highlight=False)


#-------------------------------- MENU -------------------------------------#
def menu():
    """
        Print menu for user, return menu choice
    """
    console.print("[green] (1)[/] Latest weather observation")
    console.print("[green] (2)[/] 12 hour forecast")
    console.print("[green] (3)[/] 7 day forecast")
    console.print("[green] (4)[/] 7 day detailed forecast")
    console.print("[green] (5)[/] Active weather alerts")
    console.print("[green] (6)[/] Weather alerts")
    console.print("[green] (9)[/] New location")
    console.print("[green] [Enter][/] to quit. Enter your choice: ", end="")
    menu_choice = input()
    return menu_choice


#-------------------------- MAIN PROGRAM ----------------------------#
def main():
    # Create weather object
    weather = nws_class.WeatherClass()
    # Get the location from the user
    weather.get_location()
    # Menu loop
    while True:
        # Display menu choices
        menu_choice = menu()

        # If the user presses the enter key, exit program
        if menu_choice == "":
            # Exit loop
            break

        # Get current weather and air quality
        elif menu_choice == "1":
            weather.clear_console()
            weather.get_latest_weather_observation()
            weather.process_latest_weather_observation()
            weather.display_latest_weather_observation()

        # Get 12 hour forecast
        elif menu_choice == "2":
            weather.clear_console()
            weather.get_hourly_forecast()
            weather.display_twelve_hour_forecast()

        # Get 7 day forecast
        elif menu_choice == "3":
            weather.clear_console()
            weather.get_7_day_forecast()
            weather.display_7_day_forecast()

        # Get and display 7 day detailed forecast
        elif menu_choice == "4":
            weather.clear_console()
            weather.get_7_day_forecast()
            weather.display_7_day_detailed_forecast()

        # Get and display active weather alerts
        elif menu_choice == "5":
            weather.clear_console()
            weather.get_active_weather_alerts()
            weather.display_active_weather_alerts()

        # Get and display weather alerts
        elif menu_choice == "6":
            weather.clear_console()
            weather.get_weather_alerts()
            weather.display_weather_alerts()

        # Make API call for a new location
        elif menu_choice == "9":
            weather.clear_console()
            weather.get_location()

    # Say goodbye to the user as the program exits
    weather.goodbye()


main()
