from typing import List, Optional
from pydantic import BaseModel, Field


class Weather(BaseModel):
    main: str
    description: str


class Main(BaseModel):
    temp: float
    feels_like: float = Field(alias="feels_like")


class Wind(BaseModel):
    speed: float


class Sys(BaseModel):
    sunrise: int
    sunset: int


class WeatherData(BaseModel):
    weather: List[Weather]
    main: Main
    visibility: Optional[int]
    wind: Wind
    dt: int
    sys: Sys
    timezone: int
    name: str

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"

