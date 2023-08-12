import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

api_key = os.getenv("API_KEY")

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

# A function to query the endpoint for latitudes and longitudes
def get_lat_long(city_name, state_code, country_code, API_key):
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}").json()

    data = resp[0]
    lat, lon = data.get("lat"), data.get("lon")
    return lat, lon

# A function to get current weather using the latitude and longitude of a place fetched using the previous function
def get_current_weather(lat, lon, API_key):
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric").json()
    data = WeatherData(
        main=resp.get("weather")[0].get("main"),
        description=resp.get("weather")[0].get("description"),
        icon=resp.get("weather")[0].get("icon"),
        temperature=int(resp.get("main").get("temp"))
    )

    return data

# A function to obtain the details of a place, get the latitude and longitude of the place and give the current weather update
def main(city_name, state_name, country_name):
    lat, lon = get_lat_long(city_name, state_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

if __name__ == "__main__":
    lat, lon = get_lat_long("Toronto", "ON", "Canada", api_key)
    print(get_current_weather(lat, lon, api_key))