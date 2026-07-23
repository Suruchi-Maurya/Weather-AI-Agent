import requests

from schemas.weather import LocationData, ServiceError
from services.cache import ttl_cache
from services.http import HTTP_SESSION


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


@ttl_cache(ttl_seconds=60 * 60 * 24 * 30)
def geocode_city(city: str) -> LocationData | ServiceError:
    """Resolve and cache a city location using Open-Meteo geocoding."""
    normalized_city = city.strip()
    if not normalized_city or normalized_city == "Unknown":
        return ServiceError(error="City is missing or unknown", provider="Open-Meteo")

    try:
        response = HTTP_SESSION.get(
            GEOCODING_URL,
            params={
                "name": normalized_city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            return ServiceError(error="City not found", provider="Open-Meteo")

        result = results[0]
        return LocationData(
            city=normalized_city,
            latitude=float(result["latitude"]),
            longitude=float(result["longitude"]),
            country=result.get("country", ""),
            timezone=result.get("timezone", ""),
        )
    except requests.RequestException:
        return ServiceError(
            error="Geocoding service unavailable",
            provider="Open-Meteo",
            retryable=True,
        )
    except (KeyError, TypeError, ValueError):
        return ServiceError(error="Could not geocode city", provider="Open-Meteo")
