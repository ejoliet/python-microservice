from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import requests
import json
from art import *

def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: 'config.json' file not found.")
    except json.JSONDecodeError:
        print("Error: 'config.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return {}

config = load_config()

with open('weatherCode.json', 'r') as file:
    weather_code_descriptions = json.load(file)['weatherCode']

class TomorrowIOHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_components = urlparse.parse_qs(parsed_path.query)

        # Check if city is provided
        city = query_components.get('city', None)

        if city:
            city_name = city[0]
            weather_data = self.get_weather_data(city_name)
            if weather_data:
                weather_code = weather_data['weatherCode']
                weather_data['weatherDescription'] = self.get_weather_description(weather_code)
                weather_data['ascii_art'] = self.get_ascii_art(weather_code)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response_json = json.dumps(weather_data)
                self.wfile.write(response_json.encode())
                # Log city and response
                print(f"City: {city_name}, Response: {response_json}")
            else:
                self.send_error(404, "Weather data not found.")
        else:
            self.send_error(400, "City name is required.")

    def get_weather_data(self, city):
        api_key = config.get('TOMORROW_IO_API_KEY')
        if not api_key:
            print("Error: API key not found in configuration.")
            return None
        base_url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={api_key}"

        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            return self.process_weather_data(data)
        return None
    
    def get_weather_description(self, weather_code):
        return weather_code_descriptions.get(str(weather_code), "Description not available")
    
    def process_weather_data(self, data):
        # Process and format the data as needed
        weather_info = data['data']['values']
        weather_info['city'] = data['location']['name']
        weather_info['position'] = data['location']
        #weather_info['ascii_art'] = get_ascii_art(weather_code) #text2art(str(weather_info['weatherCode']))  # ASCII Art
        return weather_info
    
    def get_ascii_art(self, weather_code):
        ascii_art_map = {
            "0": "???",
            "1000": "☀️",  # Clear, Sunny
            "1100": "🌤️",  # Mostly Clear
            "1101": "⛅",   # Partly Cloudy
            "1102": "🌥️",  # Mostly Cloudy
            "1001": "☁️",  # Cloudy
            "2000": "🌫️",  # Fog
            "2100": "🌁",   # Light Fog
            "4000": "🌦️",  # Drizzle
            "4001": "🌧️",  # Rain
            "4200": "🌦️",  # Light Rain
            "4201": "🌧️",  # Heavy Rain
            "5000": "❄️",  # Snow
            "5001": "🌨️",  # Flurries
            "5100": "🌨️",  # Light Snow
            "5101": "❄️",  # Heavy Snow
            "6000": "🧊",   # Freezing Drizzle
            "6001": "🧊",   # Freezing Rain
            "6200": "🧊",   # Light Freezing Rain
            "6201": "🧊",   # Heavy Freezing Rain
            "7000": "🌨️",  # Ice Pellets
            "7101": "🌨️",  # Heavy Ice Pellets
            "7102": "🌨️",  # Light Ice Pellets
            "8000": "⛈️",   # Thunderstorm
        }
        return ascii_art_map.get(str(weather_code), "???")

def run(server_class=HTTPServer, handler_class=TomorrowIOHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    print(f"Example URL: http://localhost:{port}/?city=Toronto")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
