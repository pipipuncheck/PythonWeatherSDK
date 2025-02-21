import threading
import time
from typing import Dict, Optional
import json

from WeatherClient import WeatherClient
from CachedWeather import CachedWeather
from WeatherClientException import WeatherClientException
from Mode import Mode


class WeatherSDK:
    _instances: Dict[str, "WeatherSDK"] = {}

    def __init__(self, api_key: str, mode: Mode):
        self.api_key = api_key
        self.mode = mode
        self.client = WeatherClient(api_key)
        self.cache: Dict[str, CachedWeather] = {}
        self._polling_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        if mode == Mode.POLLING:
            self.start_polling()

    def __str__(self):
        return f"WeatherSDK(api_key='{self.api_key}', mode={self.mode})"

    @classmethod
    def add_instance(cls, api_key: str, mode: Mode) -> "WeatherSDK":
        if api_key in cls._instances:
            raise ValueError(f"Ошибка: экземпляр с ключом '{api_key}' уже создан.")
        sdk = WeatherSDK(api_key, mode)
        cls._instances[api_key] = sdk
        return sdk

    @classmethod
    def remove_instance(cls, api_key: str):
        if api_key not in cls._instances:
            raise ValueError(f"Ошибка: экземпляр с ключом '{api_key}' не найден.")
        sdk = cls._instances.pop(api_key)
        sdk.stop_polling()

    def get_weather(self, city: str):
        if city in self.cache and not self.cache[city].is_expired():
            return self.cache[city].data
        try:
            data = self.client.fetch_weather(city)
            self.update_cache(city, data)
            return data
        except WeatherClientException as e:
            raise RuntimeError("Ошибка при получении данных о погоде") from e

    def get_weather_as_json(self, city: str) -> str:
        data = self.get_weather(city)
        return self.serialize_to_json(data)

    def serialize_to_json(self, data) -> str:
        try:
            return json.dumps(data.dict(), ensure_ascii=False)
        except Exception as e:
            raise RuntimeError("Ошибка при сериализации JSON") from e

    def update_cache(self, city: str, data):
        if len(self.cache) >= 10:
            oldest_city = next(iter(self.cache))
            del self.cache[oldest_city]
        self.cache[city] = CachedWeather(data)

    def start_polling(self):
        def poll():
            while not self._stop_event.is_set():
                for city in list(self.cache.keys()):
                    try:
                        data = self.client.fetch_weather(city)
                        self.update_cache(city, data)
                    except WeatherClientException:
                        continue
                time.sleep(600)

        self._polling_thread = threading.Thread(target=poll, daemon=True)
        self._polling_thread.start()

    def stop_polling(self):
        if self._polling_thread:
            self._stop_event.set()
            self._polling_thread.join()

