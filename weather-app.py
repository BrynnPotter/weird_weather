import requests
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

def geocode_city(city_name):
    resp = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city_name, "count": 5} )
    resp.raise_for_status()
    results = resp.json().get("results", []) #parse JSON from resp.json and pick the top match
    if not results:
        raise ValueError(f"No matches found for '{city_name}'")
    return results[0] # taking the top match

city = input(" Whos weather are you trying to see huh? ").strip()
location = geocode_city(city)
lat, lon = location["latitude"], location["longitude"]
print(f" Using coordinates: {lat}, {lon} (timezone {location.get('timezone')})")

om = openmeteo_requests.Client()
params = {

    "latitude": lat,

    "longitude": lon,

    "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],

    "current": ["temperature_2m", "relative_humidity_2m"],

    "timezone": location.get("timezone", "UTC"),

    # "response_units": {"temprature_unit": "fahrenheit"}

}

responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)

response = responses[0]

print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")

print(f"Elevation {response.Elevation()} m asl")

print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")

print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")



# Current values

current = response.Current()

current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))

current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))

current_relative_humidity_2m = next(filter(lambda x: x.Variable() == Variable.relative_humidity and x.Altitude() == 2, current_variables))



print(f"Current time {current.Time()}")

print(f"Current temperature_2m {current_temperature_2m.Value()}")

print(f"Current relative_humidity_2m {current_relative_humidity_2m.Value()}")



temp_var = current_temperature_2m

temp_value = temp_var.Value()


if temp_value > 30.0:

     print("It's a hot day! but is this messuring farenhight or celcius(its celcius but this is a growing project so something will work in here)")

elif temp_value > 20.0 :

    print("It's a nice day! or very cold i dont know yet")

else:

    print("Bring a jacket maybe, I dont know lol.")
