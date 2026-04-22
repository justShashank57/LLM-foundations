import requests
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def calculate(expression: str):
    try:
        result = eval(expression)  # ⚠️ unsafe in real systems
        return str(result)
    except Exception:
        return "Invalid expression"


def get_time(city: str):
    return f"Current time in {city} is {datetime.now().strftime('%H:%M:%S')} (PS: server's time, not actual city time)"


def check_weather(latitude, longitude):
    """Synchronous weather check using requests library"""
    import requests
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m",
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["hourly"]["temperature_2m"][0],
            "wind_speed": data["hourly"]["wind_speed_10m"][0]
        }

    except requests.RequestException as e:
        return {"error": str(e)}

TOOLS_MAP = {
    "get_time": get_time,
    "calculate": calculate,
    "check_weather": check_weather
}
