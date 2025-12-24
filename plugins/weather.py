import requests, os

def run(arg: str, cfg: dict) -> str:
    key = cfg.get("WEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")
    if not key:
        raise RuntimeError("WEATHER_API_KEY missing in config.json")
    city = arg or "Delhi"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    d = r.json()
    name = d.get("name", city)
    desc = d["weather"][0]["description"].title()
    temp = d["main"]["temp"]
    feels = d["main"]["feels_like"]
    hum = d["main"]["humidity"]
    wind = d["wind"]["speed"]
    return f"{name}: {desc}\nTemp: {temp}°C (feels {feels}°C)\nHumidity: {hum}%  Wind: {wind} m/s"
