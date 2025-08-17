import requests
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

def geocode_city(city_name):
    """
    Given a city name string, use Open-Meteo's geocoding API
    to return the top matching location data as a dict.
    Raises ValueError if no results found.
    """
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 5}
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"No matches found for '{city_name}'")
    return results[0]

def get_weather_data(location):
    """
    Given a location dict (from geocode_city), fetch current weather data.
    Returns a dict with temperature, humidity, and other info.
    """
    lat, lon = location["latitude"], location["longitude"]

    client = openmeteo_requests.Client()
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
        "current": ["temperature_2m", "relative_humidity_2m"],
        "timezone": location.get("timezone", "UTC"),
    }

    responses = client.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    current = response.Current()
    current_variables = [current.Variables(i) for i in range(current.VariablesLength())]

    temperature_var = next(
        (v for v in current_variables if v.Variable() == Variable.temperature and v.Altitude() == 2), None
    )
    humidity_var = next(
        (v for v in current_variables if v.Variable() == Variable.relative_humidity and v.Altitude() == 2), None
    )

    if temperature_var is None or humidity_var is None:
        raise RuntimeError("Could not find temperature or humidity data in the API response")

    return {
        "latitude": lat,
        "longitude": lon,
        "timezone": location.get("timezone", "UTC"),
        "temperature": temperature_var.Value(),
        "humidity": humidity_var.Value(),
        "elevation": response.Elevation(),
        "timezone_abbr": response.TimezoneAbbreviation(),
        "current_time": current.Time()
    }
