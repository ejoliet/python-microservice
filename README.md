# Python Weather Microservice

## Description

This Python microservice provides real-time weather information based on city names. It utilizes the [Tomorrow.io Weather API](https://www.tomorrow.io/weather-api/) to fetch weather data, returning details such as temperature, weather conditions, and a symbolic ASCII art representation of the current weather.

## Installation

### Prerequisites

- Python 3.x
- `requests` library (for making HTTP requests)
- An API key from Tomorrow.io

### Setup

1. **Clone the Repository**

   ```bash
   git clone [Your Repository URL]
   cd [Your Repository Directory]
   ```

2. **Install Dependencies**

   Use virtual env, create one
   ```bash
   python3 -m venv weather_env
   ```
   Then activate by executing
   ```bash
   source weather_env/bin/activate
   ```
   Deactivate:
   ```bash
   deactivate
   ```
   Use pip to install the required Python packages:

   ```bash
   pip3 install requests art json
   ```

4. **API Key Configuration**

   - Obtain an API key from [Tomorrow.io](https://www.tomorrow.io/weather-api/).
   - Create a `config.json` file in the same directory as your Python script with the following content:

     ```json
     {
       "TOMORROW_IO_API_KEY": "your_api_key_here"
     }
     ```
   - Replace `your_api_key_here` with your actual API key.
   - Ensure `config.json` is added to your `.gitignore` file to prevent it from being pushed to public repositories.

## Usage

1. **Run the Server**

   Start the microservice by running:

   ```bash
   python3 weather.py
   ```

   This will start the HTTP server on port 8000.

2. **Accessing the Service**

   To fetch weather information, access the service via a web browser or a tool like `curl` using:

   ```
   http://localhost:8000/?city=CityName
   ```

   Replace `CityName` with the desired city's name.

   Example:
   ```
   http://localhost:8000/?city=Toronto
   ```

3. **Response Format**

   The service returns a JSON object containing weather data, including temperature, weather conditions, and an ASCII representation of the current weather.

