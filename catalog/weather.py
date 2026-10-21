import requests
from django.conf import settings

def get_forecast(lat, lon):
    response = requests.get(
        f"https://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API}&q={lat},{lon}&days=3&lang=uk"
    ).json()

    if "error" in response:
        raise ValueError(response["error"]["message"])

    return response