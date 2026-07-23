import requests

from core.config import OPENWEATHER_API_KEY
from schemas.weather import AirQualityData, ServiceError
from services.cache import ttl_cache
from services.http import HTTP_SESSION


AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}


@ttl_cache(ttl_seconds=60 * 15)
def get_air_quality(
    city: str,
    latitude: float,
    longitude: float,
) -> AirQualityData | ServiceError:
    """Fetch and cache current air quality from OpenWeather."""
    if not OPENWEATHER_API_KEY:
        return ServiceError(
            error="OPENWEATHER_API_KEY is missing",
            provider="OpenWeather",
        )

    try:
        response = HTTP_SESSION.get(
            AIR_POLLUTION_URL,
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": OPENWEATHER_API_KEY,
            },
            timeout=10,
        )
        response.raise_for_status()
        current = response.json()["list"][0]
        aqi_index = int(current["main"]["aqi"])
        components = current["components"]
        return AirQualityData(
            city=city,
            aqi_index=aqi_index,
            aqi_label=AQI_LABELS.get(aqi_index, "Unknown"),
            pm2_5=float(components["pm2_5"]),
            pm10=float(components["pm10"]),
        )
    except requests.RequestException:
        return ServiceError(
            error="AQI service unavailable",
            provider="OpenWeather",
            retryable=True,
        )
    except (KeyError, TypeError, ValueError, IndexError):
        return ServiceError(
            error="AQI response was incomplete or invalid",
            provider="OpenWeather",
        )
