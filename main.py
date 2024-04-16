import requests
import os
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client

dotenv_path = find_dotenv()  # finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

OWM_KEY = os.getEnv(WEATHER_OMW_KEY)
LAT = 39.734620
LONG = -75.639610
URL = f"https://api.openweathermap.org/data/2.8/onecall"
PHONE_NUMBER = os.getEnv("WEATHER_SENDING_PHONE_NUMBER")
auth_token = os.getEnv("WEATHER_AUTH_TOKEN")
account_sid = os.getEnv("ACCOUNT_SID")
client = Client(account_sid, auth_token)

params = {
    "lat": LAT,  # Current latitude
    "lon": LONG,  # Current longitude
    "appid": OWM_KEY,
    "exclude": ["current", "minutely", "daily", "alerts"],  # Excludes these
    "units": "imperial"  # Sets units to imperial
}

weather_request = requests.get(URL, params)
weather_request.raise_for_status()
hourly_weather = weather_request.json()["hourly"][:12]

index = 0
for hour in hourly_weather:
    weather_code = hour["weather"][0]["id"]
    if int(weather_code) < 700:
        message = client.messages.create(
            from_=PHONE_NUMBER,
            body="Its going to rain",
            to=os.getEnv("WEATHER_PHONE_NUMBER")
        )
        print(message.status)
        break
