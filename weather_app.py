import requests
import json
import sys
import os

def main():
    """
    Main function to drive the program:
    - Handles user input for city names.
    - Fetches weather data from the OpenWeatherMap API.
    - Processes and displays the weather data in a readable format.
    - Provides an option to retry with a different city on error or exit.
    """
    city = user_input()  # Get user input for the city name
    try:
        information = get_api_info(city)  # Fetch weather data from the API
        if information:
            readable_information = get_readable_information(information)  # Convert data to a readable JSON format
            print(readable_information)  # Optional: print all weather data in JSON format for debugging or detailed view
            
            # Processing and displaying specific weather details
            get_location_url = generate_map_url(city)  # Generate a URL for the city's map
            temperature(information, city, get_location_url)  # Display temperature
            humidity(information)  # Display humidity
            weather_description(information)  # Display weather description and wind speed
            
            # Display the location URL (map)
            print(f'Location on map: {get_location_url}')
        else:
            print("Failed to retrieve information for the specified city.")
            again_location_input()  # Prompt user to try another city or exit
    except Exception as e:
        print(f"An error occurred: {e}")
        again_location_input()  # Handle any unexpected errors and offer retry

def user_input():
    """
    Prompts the user to enter a city name and returns the sanitized input.
    """
    city = input('Enter the city: ').title().strip()
    return city

def temperature(information, city, get_location_url):
    """
    Processes and displays the temperature in Celsius.
    """
    try:
        temp = information['main']['temp']
        temp_in_celsius = kelvin_to_celsius(temp)
        print(f'Temperature in {city} is : {temp_in_celsius:.1f}^C.')
    except KeyError:
        print("Temperature information is not available.")

def humidity(information):
    """
    Displays the humidity percentage.
    """
    try:
        h = information['main']['humidity']
        print(f'Humidity is: {h}%.')
    except KeyError:
        print("Humidity information is not available.")

def weather_description(information):
    """
    Displays the general weather description and wind speed.
    """
    try:
        description = information['weather'][0]['description']
        wind_speed = information['wind']['speed']
        print(f'Weather description: {description}, Wind speed: {wind_speed} m/sec.')
    except (KeyError, IndexError):
        print("Weather description or wind speed information is not available.")

def get_readable_information(info):
    """
    Returns a JSON string of the info dictionary, formatted for readability.
    """
    return json.dumps(info, indent=4)

def kelvin_to_celsius(K):
    """
    Converts Kelvin to Celsius.
    """
    return K - 273.15

def get_api_info(city):
    """
    Fetches the weather information for a given city from OpenWeatherMap API.
    """
    api_key = os.getenv('OPENWEATHER_API_KEY', '4ebc12f2c2438fdb9cf3b6b7a92b6586')  # Safely load the API key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_map_url(city):
    """
    Generates a URL for viewing the location on OpenStreetMap.
    """
    base_url = "https://www.openstreetmap.org/search?"
    query = f"query={city}"
    url = f"{base_url}{query}"
    return url

def again_location_input():
    """
    Prompts the user to decide if they want to try another city after an error.
    """
    again_input = input('Do you want to try another location? (yes/no): ').lower()
    if again_input == 'yes':
        main()
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
