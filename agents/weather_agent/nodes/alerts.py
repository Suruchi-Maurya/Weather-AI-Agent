from graph.state import WeatherState
from schemas.weather import EnvironmentalAlert


RISK_ORDER = {"unknown": 0, "low": 1, "moderate": 2, "high": 3}


def _alert(
    severity: str,
    title: str,
    message: str,
    source: str,
) -> EnvironmentalAlert:
    return EnvironmentalAlert(
        severity=severity,
        title=title,
        message=message,
        source=source,
    )


def evaluate_alerts_node(state: WeatherState) -> WeatherState:
    """Create deterministic safety alerts from available environmental data."""
    alerts: list[EnvironmentalAlert] = []
    weather = state.get("weather_data", {})
    forecast = state.get("forecast_data", {})
    air_quality = state.get("aqi_data", {})

    if weather and "error" not in weather:
        apparent = weather.get("apparent_temperature")
        wind_speed = weather.get("wind_speed")
        weather_code = weather.get("weather_code")
        if apparent is not None and apparent >= 40:
            alerts.append(_alert(
                "high",
                "Extreme heat",
                f"It feels like {apparent} degrees C. Heat illness is possible.",
                "weather",
            ))
        elif apparent is not None and apparent >= 35:
            alerts.append(_alert(
                "moderate",
                "Heat caution",
                f"It feels like {apparent} degrees C. Limit strenuous activity.",
                "weather",
            ))

        if wind_speed is not None and wind_speed >= 50:
            alerts.append(_alert(
                "high",
                "Strong wind",
                f"Wind speed is {wind_speed} km/h.",
                "weather",
            ))
        elif wind_speed is not None and wind_speed >= 30:
            alerts.append(_alert(
                "moderate",
                "Wind caution",
                f"Wind speed is {wind_speed} km/h.",
                "weather",
            ))

        if weather_code == 95:
            alerts.append(_alert(
                "high",
                "Thunderstorm",
                "Thunderstorms are present. Avoid exposed outdoor areas.",
                "weather",
            ))

    if forecast and "error" not in forecast:
        upcoming = forecast.get("days", [])[:3]
        max_rain = max(
            (day.get("rain_probability", 0) for day in upcoming),
            default=0,
        )
        if any(day.get("weather_code") == 95 for day in upcoming):
            alerts.append(_alert(
                "high",
                "Thunderstorm forecast",
                "A thunderstorm is forecast within the next three days.",
                "forecast",
            ))
        elif max_rain >= 80:
            alerts.append(_alert(
                "high",
                "Heavy rain likely",
                f"Rain probability reaches {max_rain}% in the next three days.",
                "forecast",
            ))
        elif max_rain >= 60:
            alerts.append(_alert(
                "moderate",
                "Rain likely",
                f"Rain probability reaches {max_rain}% in the next three days.",
                "forecast",
            ))

    if air_quality and "error" not in air_quality:
        aqi_index = air_quality.get("aqi_index")
        if aqi_index is not None and aqi_index >= 4:
            alerts.append(_alert(
                "high",
                "Poor air quality",
                "Reduce prolonged outdoor activity, especially for sensitive groups.",
                "air_quality",
            ))
        elif aqi_index == 3:
            alerts.append(_alert(
                "moderate",
                "Moderate air quality",
                "Sensitive people may want to reduce prolonged outdoor exertion.",
                "air_quality",
            ))

    risk_level = "low"
    for alert in alerts:
        if RISK_ORDER[alert.severity] > RISK_ORDER[risk_level]:
            risk_level = alert.severity

    return {
        "environmental_alerts": [alert.model_dump() for alert in alerts],
        "risk_level": risk_level,
    }
