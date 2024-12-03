"""
    Name: weather_utils.py
    Author: William A Loring
    Created: 06/20/2021
    Purpose: NWS endpoint and general weather utilities
"""
import datetime
import math


NWS_ENDPOINT = "https://api.weather.gov/"


#--------------------------- CONVERT TO CELSIUS TO FAHRENHEIT--------------------#
def celsius_to_fahrenheit(celsius):
    return round((((celsius * 9.0) / 5.0) + 32), 1)


#--------------------------- CONVERT DAY TIME -----------------------------------#
def convert_day_time(unix_time):
    """
        Convert GMT Unix timestamp to local day, month, year
    """
    # Convert Unix timestamp to Python datetime
    local_time = datetime.datetime.fromtimestamp(unix_time)

    # Format the date to hours, AM PM
    local_time = local_time.strftime("%m/%d/%Y")

    # Strip out the leading 0's
    local_time = local_time.lstrip("0")
    return local_time


#--------------------------- CONVERT HOUR TIME -----------------------------------#
def convert_hourly_time(time):
    """
        Convert GMT Unix time to local hourly time
    """
    # Convert Unix timestamp to Python datetime
    time = datetime.datetime.fromtimestamp(time)

    # Format the date to hours, AM PM
    time = time.strftime("%I:%S %p")

    # Strip out the leading 0's
    time = time.lstrip("0")
    return time


#----------------------------- CONVERT TIME --------------------------------#
def convert_time(time):
    """
        Convert GMT Unix time to local time
    """
    # Convert Unix timestamp to local Python datetime
    time = datetime.datetime.fromtimestamp(time)
    # Format the date to hours, minutes, seconds, AM PM
    time = f"{time:%I:%M:%S %p}"
    # Strip out the leading 0's: 01 becomes 1
    time = time.lstrip("0")
    # Return GMT Unix as local Python time object
    return time


#--------------------- CONVERT DEGREES TO CARDINAL ----------------------------#
def degrees_to_cardinal(degrees):
    """ Convert degrees to cardinal directions """

    # Tuple of cardinal directions clockwise for 360 degrees
    cardinal_directions = (
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    )

    # Divide 360 degrees into 16 segments 0-15
    # 22.5 degrees per segment
    # Shift incoming degrees by 11.25 to match Cardinal to Degree
    # Round down to the nearest integer
    cardinal_index = math.floor((degrees+11.25) / 22.5)

    # Take care of 348 to 360 returning 16, set to 0
    cardinal_index = cardinal_index % 16

    # Return the cardinal direction based on the tuple index
    return cardinal_directions[cardinal_index]
