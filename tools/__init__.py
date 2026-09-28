from .calculate import calculate,calculate_tool
from .weather_query import get_weather,weather_tool

TOOLS = [
    calculate_tool,
    weather_tool,
]

TOOLS_FUNCTIONS = {
    "calculator":calculate,
    "weather_query":get_weather,
}