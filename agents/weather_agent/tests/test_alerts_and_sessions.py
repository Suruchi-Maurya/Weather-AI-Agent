import tempfile
import unittest
from pathlib import Path

from nodes.alerts import evaluate_alerts_node
from persistence import database


class AlertTests(unittest.TestCase):
    def test_extreme_heat_and_poor_air_quality_produce_high_risk(self) -> None:
        result = evaluate_alerts_node({
            "weather_data": {
                "apparent_temperature": 42,
                "wind_speed": 8,
                "weather_code": 0,
            },
            "aqi_data": {"aqi_index": 4},
            "forecast_data": {"days": []},
        })
        titles = {alert["title"] for alert in result["environmental_alerts"]}
        self.assertEqual(result["risk_level"], "high")
        self.assertIn("Extreme heat", titles)
        self.assertIn("Poor air quality", titles)


class SessionTests(unittest.TestCase):
    def test_new_session_starts_with_zero_messages(self) -> None:
        original_path = database.DB_PATH
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            database.DB_PATH = Path(temp_dir) / "test.db"
            try:
                database.init_db()
                database.start_new_session("user-a")
                stats = database.get_session_stats("user-a")
                self.assertEqual(stats["message_count"], 0)

                database.upsert_session("user-a")
                stats = database.get_session_stats("user-a")
                self.assertEqual(stats["message_count"], 1)
            finally:
                database.DB_PATH = original_path


if __name__ == "__main__":
    unittest.main()
