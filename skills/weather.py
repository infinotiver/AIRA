import requests
from urllib.parse import quote


def get_weather(api_key, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",  # You can change to 'imperial' for Fahrenheit
    }

    try:
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        print(complete_url)
        response = requests.get(complete_url)
        print(response)
        data = response.json()
        responses = []
        if response.status_code == 200:
            main_weather = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (
                f"The weather in {city_name} is {main_weather} ({description}). "
                f"The temperature is {temperature}°C, humidity is {humidity}%, and wind speed is {wind_speed} m/s."
            )
            responses.append(weather_info)

        else:
            responses.append(
                f"Sorry, there was an issue fetching weather information for {city_name}."
            )
        return responses
    except Exception as e:
        return f"An error occurred: {e}"
