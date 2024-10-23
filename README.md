# Real-Time Weather Monitoring System

This project is a Real-Time Weather Monitoring System that provides continuous weather updates and insights by integrating with the OpenWeatherMap API. The system includes features for live weather data, weather forecasts, air pollution monitoring, and the ability to perform basic aggregations and set temperature thresholds for alerts.

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy (SQLite)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **APIs:** OpenWeatherMap API (Live Weather, Weather Forecast, Air Pollution)

## Key Functionalities

1. **Basic Aggregations:**
   - Provides basic weather data aggregations (average, maximum, minimum temperatures, dominant weather condition) for a list of predefined cities.
   - Users can view temperatures in Celsius (default), Fahrenheit, or Kelvin.

2. **Thresholds and Alerts:**
   - Users can set a threshold temperature (default is 35°C).
   - A toast alert appears on the top-right corner of the webpage if the temperature crosses the threshold value twice.
   - This feature is available for predefined cities only.

3. **Visualization:**
   - Weather data is presented in table format for easy viewing.
   - Alerts are shown using CSS Bootstrap toasts, which are small pop-up notifications.
   - The page automatically reloads every 5 minutes to fetch and display updated data.

4. **Weather Forecast:**
   - A 5-day weather forecast is provided via the OpenWeatherMap Forecast API.
   - Users can search for the forecast by city name or ZIP code.

5. **Search A City:**
   - Users can search for weather information by entering a city name or ZIP code.
   - The search results, including temperature, humidity, and other relevant data, are displayed on a new page.

6. **Air Pollution:**
   - This module utilizes the OpenWeatherMap Air Pollution API to show information about pollutants in a specific city.
   - Users can also retrieve a 5-day air pollution forecast by providing the city name or ZIP code.

7. **Manipulation of Basic Cities:**
   - Users can add or remove cities from the predefined list.
   - When a new city is added, its data is stored in the database for future use.
   - Deleting a city only removes it from the current list but retains its data in the database for potential future use.

## Product Design

The system is based on four main components: **Frontend**, **Backend**, **Database**, and **API**.

### 1. User Interface (UI)
- **HTML**: Structures the webpage for displaying weather data and user interactions.
- **CSS (Bootstrap)**: Ensures a responsive and visually appealing design, with easy-to-use buttons and forms.
- **JavaScript**: Handles the functionality of the buttons and dynamic data updates on the webpage.

### 2. Backend
- **Flask (Python)**: A lightweight web framework used to build the backend of the application.
- The backend handles data processing, API calls, and interaction with the database, while ensuring modular code for ease of maintenance.

### 3. Database
- **SQLAlchemy (SQLite)**: Manages database interactions for storing and retrieving data.
- The database stores 5-minute interval weather data and daily summaries for predefined cities.
  
### 4. API
- **OpenWeatherMap API**: Provides weather data (live weather updates, 5-day forecasts) and air pollution information.
- APIs are free to use and deliver detailed weather information, enabling the system to function in real-time.

## Installation

To get started with this project, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/Koushik-p-g-v/Weather-Monitoring-System.git
2. Navigate into project repository:
   ```bash
   cd Weather-Monitoring-System
3. Create and Activate a virtual environment:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
4. Install Dependencies:
   ```bash
   pip install -r requirements.txt
5. Run the Application:
   ```bash
   python app.py
6. Open a browser and navigate to `http://127.0.0.1:5000` to use the Rule Engine Application.

## API Setup
- The application uses OpenWeatherMap APIs to fetch real-time weather, 5-day forecasts, and air pollution data.

## Features in Detail

1. **Basic Aggregations** 
   - The system aggregates weather data such as average, maximum, and minimum temperatures.
   - These aggregations are displayed for predefined cities, and users can toggle between Celsius, Fahrenheit, and Kelvin units.
2. **Threshold Alerts** 
   - Users can set a temperature threshold, which triggers a Bootstrap toast notification when exceeded.
   - The system checks for this condition twice before displaying an alert, ensuring no false positives.
3. **Weather Forecast** 
   - Users can enter a city name or ZIP code to receive a 5-day weather forecast.
   - Data includes temperature, weather conditions, humidity, and other key parameters.
4. **Air Pollution** 
   - Air pollution data is available for any city or ZIP code entered by the user.
   - The system provides information on pollutants and offers a 5-day pollution forecast.
5. **City Manipulation**
   - Users can add new cities to the list, and their weather data will be stored in the database for future updates.
   - Although cities can be removed from the current list, their data remains in the database for future reference.
