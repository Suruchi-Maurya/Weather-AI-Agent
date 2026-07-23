import requests

from schemas.weather import (
    CurrentWeather,
    ForecastData,
    ForecastDay,
    ServiceError,
)
from services.cache import ttl_cache
from services.http import HTTP_SESSION


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@ttl_cache(ttl_seconds=60 * 10)
def get_current_weather(
    city: str,
    latitude: float,
    longitude: float,
) -> CurrentWeather | ServiceError:
    """Fetch and cache current conditions from Open-Meteo."""
    try:
        response = HTTP_SESSION.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,apparent_temperature,"
                    "relative_humidity_2m,wind_speed_10m,weather_code"
                ),
            },
            timeout=10,
        )
        response.raise_for_status()
        current = response.json()["current"]
        return CurrentWeather(
            city=city,
            temperature=float(current["temperature_2m"]),
            apparent_temperature=float(current["apparent_temperature"]),
            humidity=int(current["relative_humidity_2m"]),
            wind_speed=float(current["wind_speed_10m"]),
            weather_code=int(current["weather_code"]),
        )
    except requests.RequestException:
        return ServiceError(
            error="Weather service unavailable",
            provider="Open-Meteo",
            retryable=True,
        )
    except (KeyError, TypeError, ValueError):
        return ServiceError(
            error="Weather response was incomplete or invalid",
            provider="Open-Meteo",
        )


@ttl_cache(ttl_seconds=60 * 30)
def get_forecast(
    city: str,
    latitude: float,
    longitude: float,
) -> ForecastData | ServiceError:
    """Fetch and cache a seven-day forecast from Open-Meteo."""
    try:
        response = HTTP_SESSION.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timezone": "auto",
                "forecast_days": 7,
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_probability_max,weather_code"
                ),
            },
            timeout=10,
        )
        response.raise_for_status()
        daily = response.json()["daily"]
        days = [
            ForecastDay(
                date=str(date),
                max_temp=float(daily["temperature_2m_max"][index]),
                min_temp=float(daily["temperature_2m_min"][index]),
                rain_probability=int(daily["precipitation_probability_max"][index]),
                weather_code=int(daily["weather_code"][index]),
            )
            for index, date in enumerate(daily["time"])
        ]
        return ForecastData(city=city, days=days)
    except requests.RequestException:
        return ServiceError(
            error="Forecast service unavailable",
            provider="Open-Meteo",
            retryable=True,
        )
    except (KeyError, TypeError, ValueError, IndexError):
        return ServiceError(
            error="Forecast response was incomplete or invalid",
            provider="Open-Meteo",
        )
