"""
    Name: geocode_geopy.py
    Author: William A Loring
    Created: 07/10/2021
    Purpose: Geocode using Nominatim from geopy
"""

# Windows: pip install geopy
# Linux: pip3 install geopy
# Import Nominatim to use OpenStreetMap's geocoding service
from geopy.geocoders import Nominatim


def main():
    # Test forward geocode
    city = input("Enter City: ")
    state = input("Enter State: ")
    country = input("Enter Country: ")
    print(geocode(city, state, country))

    # Test reverse geocode
    LAT = 41.8666
    LON = -103.6672
    print(reverse_geocode(LAT, LON))


# --------------------------- GEOCODE ------------------------------------ #
def geocode(city, state, country):
    """Get latitude, longitude, and address using geopy from city, state, and country.
    Args:
        city (str): The name of the city.
        state (str): The name of the state.
        country (str): The name of the country.
    Returns:
        tuple: tuple containing latitude (float), longitude (float), address (str).
    Raises:
        Exception: If an error occurs during geocoding,
        an exception is raised and an error message is printed.
    """
    try:
        # Create geolocator object with Nominatim geocode service
        # Nominatim is a free geolocater that uses openstreetmaps.org
        geolocator = Nominatim(user_agent="locate_me")

        # Create location dictionary for geocode request
        location = {
            "city": city,
            "state": state,
            "country": country
        }
        # Get geocode object with location data
        # lat, lng, address
        geo_location = geolocator.geocode(location)

        if geo_location is None:
            raise Exception("Geocoding failed: location not found.")

        # Uncomment for testing as a program
        # print(geo_location.raw)
        # print(geo_location.address)
        # print((geo_location.latitude, geo_location.longitude))

        # Return geocode location information to calling program
        return (
            geo_location.latitude,
            geo_location.longitude,
            geo_location.address
        )
    except Exception as e:
        print(f"An error occurred while geocoding: {e}")
        # Print exception message
        print(e)


# --------------------------- REVERSE GEOCODE ---------------------------- #
def reverse_geocode(lat, lon):
    """
    Reverse geocode from latitude and longitude using geopy.
    This function takes latitude and longitude as input and returns the address
    corresponding to that location using the geopy library's Nominatim service.
    Args:
        lat (float): The latitude of the location to reverse geocode.
        lon (float): The longitude of the location to reverse geocode.
    Returns:
        str: The address corresponding to the given latitude and longitude.
    Raises:
        Exception: If an error occurs during the reverse geocoding process.
    """
    try:
        # Create geolocator object
        geolocator = Nominatim(user_agent="locate_me")
        address = geolocator.reverse((lat, lon), exactly_one=True, zoom=10)

        # Uncomment For testing as a program
        # print(address)

        if address is None:
            return "Address not found"
        return address
        # print(address)

    except Exception as e:
        print(
            f"An error occurred while reverse geocoding for coordinates ({lat}, {lon}).")
        # Print exception message
        print(e)


# If a standalone program, call the main function
# Else, use as a module
if __name__ == '__main__':
    main()
