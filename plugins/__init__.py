from .weather import run as weather
from .news import run as news
from .system_control import run as system
from .google_calendar import run as gcal

registry = {
    "weather": weather,
    "news": news,
    "system": system,
    "gcal": gcal,
}
