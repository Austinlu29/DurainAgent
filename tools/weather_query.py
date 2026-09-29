import requests

def get_weather(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name":city,
        "count":1,
        "language":"zh",
        "format":"json",
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params,
        timeout = 10,
    )

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"找不到城市{city}"

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude":latitude,
        "longitude":longitude,
        "current":"temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "temperature_unit":"celsius",
        "wind_speed_unit":"kmh",
        "timezone":"auto",
    }
    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout = 10,
    )

    weather_data = weather_response.json()

    # print("天气API返回：")
    # print(weather_data)

    current = weather_data["current"]

    return {
        "城市":location["name"],
        "温度":current["temperature_2m"],
        "湿度": current["relative_humidity_2m"],
        "天气代码": current["weather_code"],
        "风速": current["wind_speed_10m"],
    }

weather_tool = {
    "type":"function",
    "function":{
        "name":"weather_query",
        "description":"查询地方天气",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string",
                },
            },
        },
        "required":["city"],
    }
}