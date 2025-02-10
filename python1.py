import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use an environment variable for API security
API_KEY = os.getenv("OPENWEATHER_API_KEY", "950fa7669aa2c70f8edb4a06fc38398f")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cache to store weather data for cities
weather_cache = {}

def get_weather(city):
    # Check if the city data is already cached
    if city in weather_cache:
        logging.info(f"Fetching weather data for {city} from cache.")
        return weather_cache[city]

    params = {"q": city, "appid": API_KEY, "units": "metric"}  # Fetch in Celsius
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        weather_info = {
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"]
        }

        # Cache the weather data
        weather_cache[city] = weather_info
        return weather_info

    except requests.exceptions.HTTPError as http_err:
        logging.error("Invalid city name. Please try again.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def display_weather(city, weather_info):
    if weather_info:
        print(f"\n🌍 City Name: {city.capitalize()}")
        print(f"🌤️ Weather: {weather_info['description'].capitalize()}")
        print(f"🌡️ Temperature: {weather_info['temp']}°C")
        print(f"💧 Humidity: {weather_info['humidity']}%")
        print(f"💨 Wind Speed: {weather_info['wind_speed']} m/s")
        print(f"📏 Pressure: {weather_info['pressure']} hPa")
    else:
        print("\n Unable to retrieve weather data.")

def main():
    print("Welcome to the Weather App! 🌦️")
    while True:
        print("\nMenu:")
        print("1. Get Weather")
        print("2. Exit")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            city_name = input("Enter city name: ").strip()
            if city_name:
                weather_info = get_weather(city_name)
                display_weather(city_name, weather_info)
            else:
                print("\n⚠️ Please enter a valid city name.")
        elif choice == "2":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n⚠️ Invalid choice. Please select 1 or 2.")

if _name_ == "_main_":
    main()
