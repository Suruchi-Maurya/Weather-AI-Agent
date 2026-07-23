import unittest
from unittest.mock import MagicMock, patch

from schemas.weather import LocationData, ServiceError
from services.cache import ttl_cache
from services.geocoding import geocode_city
from services.http import build_retry_session


class ServiceInfrastructureTests(unittest.TestCase):
    def test_ttl_cache_reuses_success_and_skips_errors(self) -> None:
        calls = {"success": 0, "error": 0}

        @ttl_cache(ttl_seconds=60)
        def successful(value: str) -> LocationData:
            calls["success"] += 1
            return LocationData(city=value, latitude=1, longitude=2)

        @ttl_cache(ttl_seconds=60)
        def failing(value: str) -> ServiceError:
            calls["error"] += 1
            return ServiceError(error=value)

        successful("Delhi")
        successful("Delhi")
        failing("temporary")
        failing("temporary")
        self.assertEqual(calls, {"success": 1, "error": 2})

    @patch("services.geocoding.HTTP_SESSION.get")
    def test_geocoding_returns_typed_location(self, mock_get) -> None:
        geocode_city.cache_clear()
        response = MagicMock()
        response.json.return_value = {
            "results": [{
                "latitude": 28.61,
                "longitude": 77.21,
                "country": "India",
                "timezone": "Asia/Kolkata",
            }]
        }
        mock_get.return_value = response

        result = geocode_city("Delhi")
        self.assertIsInstance(result, LocationData)
        self.assertEqual(result.country, "India")

    def test_http_session_has_retry_policy(self) -> None:
        session = build_retry_session()
        adapter = session.get_adapter("https://")
        self.assertEqual(adapter.max_retries.total, 2)
        self.assertIn(503, adapter.max_retries.status_forcelist)


if __name__ == "__main__":
    unittest.main()
