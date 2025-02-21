import json
import unittest
from unittest.mock import patch
from time import sleep

from PythonWeatherSDK import WeatherSDKForTesting
from PythonWeatherSDK.Mode import Mode


class WeatherSDKTest(unittest.TestCase):

    API_KEY = "your_api_key"
    mock_web_server_url = 'http://localhost:8080/'
    sdk = None

    def setUp(cls):
        cls.sdk = WeatherSDKForTesting.add_instance("test-api-key", Mode.POLLING, cls.mock_web_server_url)

    def tearDown(cls):
        WeatherSDKForTesting.clear_instances_for_testing()

    @patch('requests.get')
    def test_add_instance_should_create_new_sdk_instance(self, mock_get):
        sdk = WeatherSDKForTesting.add_instance(self.API_KEY, Mode.ON_DEMAND, self.mock_web_server_url)
        self.assertIsNotNone(sdk)

    @patch('requests.get')
    def test_add_instance_should_throw_exception_when_api_key_already_exists(self, mock_get):
        WeatherSDKForTesting.add_instance(self.API_KEY, Mode.ON_DEMAND, self.mock_web_server_url)
        with self.assertRaises(ValueError) as context:
            WeatherSDKForTesting.add_instance(self.API_KEY, Mode.ON_DEMAND, self.mock_web_server_url)
        self.assertTrue("Ошибка: экземпляр с ключом 'your_api_key' уже создан." in str(context.exception))

    @patch('requests.get')
    def test_remove_instance_should_delete_instance(self, mock_get):
        WeatherSDKForTesting.add_instance(self.API_KEY, Mode.ON_DEMAND, self.mock_web_server_url)
        WeatherSDKForTesting.remove_instance(self.API_KEY)

        with self.assertRaises(ValueError) as context:
            WeatherSDKForTesting.remove_instance(self.API_KEY)
        self.assertTrue("Ошибка: экземпляр с ключом 'your_api_key' не найден." in str(context.exception))

    @patch('requests.get')
    def test_get_weather_should_return_cached_data_when_not_expired(self, mock_get):
        weather_json = json.dumps({
            "weather": [{"description": "clear sky", "PythonWeatherSDK": "Clear"}],
            "PythonWeatherSDK": {"temp": 20, "humidity": 65, "feels_like": 18},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"country": "GB", "sunrise": 1630419354, "sunset": 1630473684},
            "timezone": 3600,
            "name": "London",
            "dt": 1630425600
        })

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(weather_json)

        data = self.sdk.get_weather("London")
        self.assertIsNotNone(data)
        self.assertEqual(data.name, "London")

        cached_data = self.sdk.get_weather("London")
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data.name, "London")

    @patch('requests.get')
    def test_get_weather_should_fetch_new_data_when_cache_expired(self, mock_get):
        old_weather_json = json.dumps({
            "weather": [{"description": "clear sky", "PythonWeatherSDK": "Clear"}],
            "PythonWeatherSDK": {"temp": 20, "humidity": 65, "feels_like": 18},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"country": "FR", "sunrise": 1630419354, "sunset": 1630473684},
            "timezone": 3600,
            "name": "Paris",
            "dt": 1630425600
        })
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(old_weather_json)

        old_data = self.sdk.get_weather("Paris")
        sleep(1)

        new_weather_json = json.dumps({
            "weather": [{"description": "light rain", "PythonWeatherSDK": "Rain"}],
            "PythonWeatherSDK": {"temp": 18, "humidity": 70, "feels_like": 16},
            "visibility": 8000,
            "wind": {"speed": 6, "deg": 190},
            "sys": {"country": "FR", "sunrise": 1630420000, "sunset": 1630475000},
            "timezone": 3600,
            "name": "Paris",
            "dt": 1630426600
        })
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(new_weather_json)

        new_data = self.sdk.get_weather("Paris")

        self.assertIsNotNone(new_data)
        self.assertEqual(new_data.name, "Paris")
        self.assertNotEqual(old_data.dt, new_data.dt)

    @patch('requests.get')
    def test_get_weather_as_json_should_return_valid_json(self, mock_get):
        weather_json = json.dumps({
            "weather": [{"description": "clear sky", "PythonWeatherSDK": "Clear"}],
            "PythonWeatherSDK": {"temp": 20, "humidity": 65, "feels_like": 18},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"country": "DE", "sunrise": 1630419354, "sunset": 1630473684},
            "timezone": 3600,
            "name": "Berlin",
            "dt": 1630425600
        })

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(weather_json)

        json_data = self.sdk.get_weather_as_json("Berlin")

        data = json.loads(json_data)

        self.assertIsNotNone(json_data)
        self.assertEqual(data['name'], 'Berlin')
        self.assertEqual(data['dt'], 1630425600)
        self.assertIn('weather', data)
        self.assertIn('PythonWeatherSDK', data)

    @patch('requests.get')
    def test_start_polling_should_update_weather_automatically(self, mock_get):
        weather_json = json.dumps({
            "weather": [{"description": "clear sky", "PythonWeatherSDK": "Clear"}],
            "PythonWeatherSDK": {"temp": 20, "feels_like": 18},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"country": "JP", "sunrise": 1630419354, "sunset": 1630473684},
            "timezone": 3600,
            "name": "Tokyo",
            "dt": 1630425600
        })

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(weather_json)

        self.sdk.get_weather("Tokyo")
        sleep(0.5)

        updated_weather_json = json.dumps({
            "weather": [{"description": "clear sky", "PythonWeatherSDK": "Clear"}],
            "PythonWeatherSDK": {"temp": 22, "feels_like": 19},
            "visibility": 10000,
            "wind": {"speed": 5, "deg": 180},
            "sys": {"country": "JP", "sunrise": 1630419354, "sunset": 1630473684},
            "timezone": 3600,
            "name": "Tokyo",
            "dt": 1630426600
        })

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(updated_weather_json)

        updated_data = self.sdk.get_weather("Tokyo")

        self.assertIsNotNone(updated_data)
        self.assertEqual(updated_data.name, "Tokyo")


if __name__ == '__main__':
    unittest.main()
