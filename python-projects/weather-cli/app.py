import json
import requests

BASE_URL = "https://api.weatherapi.com/v1/current.json"
KEY = "ce23e409e48a4dc5b1f74944263107"

def fetch_weather(city: str):
    payload = {
        "key": KEY,
        "q": city
    }
    try:
        response = requests.get(BASE_URL, params=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        location = data["location"]
        current = data["current"]
        message = f"""
            Country: {location["country"]},
            Location: {location["name"]},
            Local Time: {location["localtime"]},
            Condition: {current["condition"]["text"]},
            Temperature: {current["temp_c"]}°C
        """
        print(message)
    except requests.exceptions.HTTPError:
        print("Failed to retrieve data")
    except requests.exceptions.ConnectionError:
        print("Internet failed to connect")
    except requests.exceptions.Timeout:
        print("Timeout")
    except KeyError:
        print("Data failed to parse")

def main():
    print("Welcome to Weather CLI")
    print("Please enter a city name and type q to exit")

    while True:
        city = input("City Name: ")
        if not city.strip():
            print("Invalid input")
            continue
        if city.lower() == "q":
            print("Exit successfully")
            break
        fetch_weather(city)

if __name__ == "__main__":
    main()
