# PythonWeatherSDK

PythonWeatherSDK is a Java library for retrieving weather data from the OpenWeather API.

___
## Features
✅ Obtain current weather by city name  
✅ Data caching (10 minutes)  
✅ Two modes of operation:
- `ON_DEMAND` — data update only on request
- `POLLING` — automatic update every 10 minutes

✅ Flexibility: you can create several SDK instances with different API keys.

___

## Quick start

**Step 1.** Paste into the terminal in the directory where the project is located

```cmd
pip install git+https://github.com/pipipuncheck/PythonWeatherSDK.git@master
```
___
## Usage Example
+ Creating an SDK instance:

    + if you want "ON_DEMAND" mode
    ```python
    sdk = WeatherSDK.add_instance("YOUR_API_KEY", Mode.ON_DEMAND)
    ```
    + "POLLING" mode
    ```python
    sdk = WeatherSDK.add_instance("YOUR_API_KEY", Mode.POLLING)
    ```
+ Obtaining weather data:
    + as python object:
    ```python
    weather = sdk.get_weather("City");
    ```
    + as json object:
    ```python
    weather = sdk.get_weather_as_json("City")
    ```
+ Deleting an instance:
```python
WeatherSDK.remove_instance("YOUR_API_KEY")
```
