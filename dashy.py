import datetime
import json
import random
import re
import requests
import string
import time
from geopy.geocoders import Nominatim

hits = {}
home_latitude = 40.730610
home_longitude = -73.935242
while True:
    try:
        # Current time
        now = re.findall(r"\d{1,2}:\d{1,2}", str(datetime.datetime.now()))[0]
        hits.update({"current_time": now})
        
        # ISS
        agent = "".join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(8,35))])
        iss = requests.get("http://api.open-notify.org/iss-now.json",timeout=10).json()
        geolocator = Nominatim(user_agent=agent)
        latitude = iss["iss_position"]["latitude"]
        longitude = iss["iss_position"]["longitude"]
        location = geolocator.reverse((latitude, longitude), language="en")

        if location:
            hits.update({"iss": f'{location.raw["address"]["state"]}, {location.raw["address"]["country"]}'})

        else:
            hits.update({"iss": "Ocean or uninhabited area"})

    except:
        pass

    try:
        # Weather
        gather_weather = requests.get(f"https://api.weather.gov/points/{home_latitude},{home_longitude}",timeout=10).text
        gather_weather = json.loads(gather_weather)["properties"]["forecastHourly"]
        weather = requests.get(gather_weather).text

        current_forecast = json.loads(weather)["properties"]["periods"][0]["shortForecast"]
        current_temperature = json.loads(weather)["properties"]["periods"][0]["temperature"]
        current_wind = json.loads(weather)["properties"]["periods"][0]["windSpeed"] + " " + json.loads(weather)["properties"]["periods"][0]["windDirection"]

        hits.update({"weather_forecast": current_forecast})
        hits.update({"weather_temperature": current_temperature})
        hits.update({"weather_wind": current_wind})

    except:
        pass

    # display json
    results = json.dumps(hits, indent=4)
    print(results)

    time.sleep(73)
