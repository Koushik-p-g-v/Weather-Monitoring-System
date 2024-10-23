import requests
from datetime import datetime
from sqlalchemy import func
from models import WeatherData, DailyWeatherSummary, db  # Only import models and db
from config import Config

def temp_convert(temp_k,unit):
    if unit=="C":
        return temp_k - 273.15
    elif unit=="F":
        return (9/5)*(temp_k-273.15)+32

def fetch_weather_data(city,unit='K'):
    params = {
        'q': city,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    response = requests.get(Config.BASE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if unit=='K':
            return {
            'city': city,
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'main': data['weather'][0]['main'],
            'timestamp': datetime(data['dt'])
        }
        else:
            return {
            'city': city,
            'temp': temp_convert(data['main']['temp'], unit),
            'feels_like': temp_convert(data['main']['feels_like'], unit),
            'main': data['weather'][0]['main'],
            'timestamp': datetime(data['dt'])
        }
    return None

def store_weather_data(weather_data):
    record = WeatherData(
        city=weather_data['city'],
        temp=weather_data['temp'],
        feels_like=weather_data['feels_like'],
        main=weather_data['main'],
        timestamp=weather_data['timestamp']
    )
    db.session.add(record)
    db.session.commit()

def rollup_daily_summaries():
    # For each city, calculate the aggregates
    for city in Config.METROS:
        records = WeatherData.query.filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == datetime.utcnow().date()
        ).all()

        if records:
            avg_temp = sum([r.temp for r in records]) / len(records)
            max_temp = max([r.temp for r in records])
            min_temp = min([r.temp for r in records])
            dominant_weather = max(set([r.main for r in records]), key=[r.main for r in records].count)

            summary = DailyWeatherSummary(
                city=city,
                date=datetime.utcnow().date(),
                avg_temp=avg_temp,
                max_temp=max_temp,
                min_temp=min_temp,
                dominant_weather=dominant_weather
            )
            db.session.add(summary)
            db.session.commit()

def check_alerts(weather_data):
    if weather_data['temp'] > Config.ALERT_THRESHOLD_TEMP:
        print(f"ALERT: High temperature in {weather_data['city']}! Current temperature: {weather_data['temp']}°C")
        # Send email or notification logic (if needed)
