import unittest
from unittest.mock import patch

from graph.routing import route_after_location, route_after_router
from nodes.location import resolve_location_node
from nodes.weather import fetch_weather_node
from schemas.weather import CurrentWeather, LocationData


class GraphFlowTests(unittest.TestCase):
    def test_weather_queries_resolve_location_before_data_nodes(self) -> None:
        state = {"intent": "weather", "required_nodes": ["weather"]}
        self.assertEqual(route_after_router(state), "location")
        self.assertEqual(route_after_location(state), "weather")

    def test_combined_queries_fan_out_after_location(self) -> None:
        state = {
            "intent": "combined",
            "required_nodes": ["weather", "forecast", "air_quality"],
        }
        self.assertEqual(route_after_router(state), "location")
        self.assertEqual(
            route_after_location(state),
            ["weather", "forecast", "air_quality"],
        )

    @patch("nodes.location.geocode_city")
    def test_location_is_resolved_once_into_state(self, mock_geocode) -> None:
        mock_geocode.return_value = LocationData(
            city="Delhi",
            latitude=28.61,
            longitude=77.21,
            country="India",
            timezone="Asia/Kolkata",
        )
        result = resolve_location_node({"city": "Delhi"})
        self.assertEqual(result["location_data"]["latitude"], 28.61)
        mock_geocode.assert_called_once_with("Delhi")

    @patch("nodes.weather.get_current_weather")
    def test_weather_node_passes_shared_coordinates(self, mock_weather) -> None:
        mock_weather.return_value = CurrentWeather(
            city="Delhi",
            temperature=31,
            apparent_temperature=34,
            humidity=55,
            wind_speed=8,
            weather_code=0,
        )
        state = {
            "city": "Delhi",
            "location_data": {
                "city": "Delhi",
                "latitude": 28.61,
                "longitude": 77.21,
                "country": "India",
                "timezone": "Asia/Kolkata",
            },
        }
        result = fetch_weather_node(state)
        self.assertEqual(result["weather_summary"]["condition"], "clear skies")
        mock_weather.assert_called_once_with("Delhi", 28.61, 77.21)


if __name__ == "__main__":
    unittest.main()
