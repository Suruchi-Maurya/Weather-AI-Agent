from typing import Literal

from pydantic import BaseModel, Field


class ServiceError(BaseModel):
    error: str
    provider: str = ""
    retryable: bool = False


class LocationData(BaseModel):
    city: str
    latitude: float
    longitude: float
    country: str = ""
    timezone: str = ""


class CurrentWeather(BaseModel):
    city: str
    temperature: float
    apparent_temperature: float
    humidity: int
    wind_speed: float
    weather_code: int


class ForecastDay(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    rain_probability: int
    weather_code: int


class ForecastData(BaseModel):
    city: str
    days: list[ForecastDay] = Field(default_factory=list)


class AirQualityData(BaseModel):
    city: str
    aqi_index: int
    aqi_label: str
    pm2_5: float
    pm10: float


class WeatherSummary(BaseModel):
    city: str
    temperature: float | None = None
    apparent_temperature: float | None = None
    humidity: int | None = None
    wind_speed: float | None = None
    condition: str = "unknown conditions"
    error: str | None = None


class AQISummary(BaseModel):
    city: str
    aqi_index: int | None = None
    aqi_label: str = "Unknown"
    pm2_5: float | None = None
    pm10: float | None = None
    error: str | None = None


class EnvironmentalAlert(BaseModel):
    severity: Literal["moderate", "high"]
    title: str
    message: str
    source: Literal["weather", "forecast", "air_quality"]


class MapData(BaseModel):
    city: str
    lat: float
    lon: float
    temperature: float | str = ""
    aqi_label: str = ""
    description: str = "unknown conditions"
    rain_probability: int | str = ""
