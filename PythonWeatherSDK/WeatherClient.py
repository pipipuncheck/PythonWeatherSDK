import requests
from requests.exceptions import RequestException

from PythonWeatherSDK.WeatherData import WeatherData
from PythonWeatherSDK.WeatherClientException import WeatherClientException


class WeatherClient:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_weather(self, city: str) -> WeatherData:
        url = f"{self.BASE_URL}?q={city}&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise WeatherClientException(f"Error fetching weather: {response.text}")

            data = response.json()
            return WeatherData(**data)
        except RequestException as e:
            raise WeatherClientException("Network error while fetching weather data", e)
