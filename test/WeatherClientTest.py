import unittest
from unittest.mock import patch

from PythonWeatherSDK.WeatherClientException import WeatherClientException
from PythonWeatherSDK import WeatherClientForTesting


class WeatherClientTest(unittest.TestCase):

    def setUp(self):
        self.mock_web_server_url = 'http://localhost:8080/'
        self.weather_client_for_testing = WeatherClientForTesting('test-api-key', self.mock_web_server_url)

    @patch('requests.get')
    def test_fetch_weather_success(self, mock_get):
        weather_json = '''{
            "weather": [{"PythonWeatherSDK": "Clear", "description": "clear sky"}],
            "PythonWeatherSDK": {"temp": 20.5, "feels_like": 19.0},
            "visibility": 10000,
            "wind": {"speed": 5.1},
            "dt": 1618317045,
            "sys": {"sunrise": 1618301045, "sunset": 1618354200},
            "timezone": 10800,
            "name": "London"
        }'''

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = eval(weather_json)

        weather_data = self.weather_client_for_testing.fetch_weather("London")

        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data.main.temp, 20.5)
        self.assertEqual(weather_data.weather[0].description, "clear sky")

    @patch('requests.get')
    def test_fetch_weather_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        with self.assertRaises(WeatherClientException):
            self.weather_client_for_testing.fetch_weather("London")


if __name__ == '__main__':
    unittest.main()
