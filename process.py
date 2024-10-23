import requests
import datetime
from datetime import date
from sqlalchemy import func
from models import WeatherData, DailyWeatherSummary, db  # Only import models and db
from config import Config



def temp_convert(temp_k,unit):
    if unit=="C":
        return temp_k - 273.15
    elif unit=="F":
        return (9/5)*(temp_k-273.15)+32
    else:
        return temp_k

def fetch_weather_data(city, unit='K'):
    params = {
        'q': city,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    response = requests.get(Config.BASE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        t=data['main']['temp'] -273.15
        if t > Config.ALERT_THRESHOLD_TEMP:
            violation=True
        else:
            violation=False
        if unit=='K':
            return {
            'city': city,
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'max_temp': data['main']['temp_max'],
            'min_temp': data['main']['temp_min'],
            'main': data['weather'][0]['main'],
            'timestamp': datetime.datetime.fromtimestamp(data['dt']).date(),
            'violation': violation
        }
        else:
            temp=temp_convert(data['main']['temp'], unit)
            ftemp=temp_convert(data['main']['feels_like'], unit)
            max_temp=temp_convert(data['main']['temp_max'], unit)
            min_temp=temp_convert(data['main']['temp_min'], unit)
            return {
            'city': city,
            'temp': temp,
            'feels_like': ftemp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'main': data['weather'][0]['main'],
            'timestamp': datetime.datetime.fromtimestamp(data['dt']).date(),
            'violation': violation
        }
    return None

def search_city_summaries(s):
    if s.isnumeric():
        city=s+',IN'
    else:
        city=s
    unit='C'
    params = {
        'q': city,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    response = requests.get(Config.BASE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
        'city': data['name'],
        'temp': temp_convert(data['main']['temp'], unit),
        'ftemp':temp_convert(data['main']['feels_like'], unit),
        'max_temp': temp_convert(data['main']['temp_max'], unit),
        'min_temp': temp_convert(data['main']['temp_min'], unit),
        'humidity': data['main']['humidity'],
        'weather_des': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'timestamp': datetime.datetime.fromtimestamp(data['dt']).date()
        }
    return None

def get_weather_forecast(s):
    if s.isnumeric():
        city=s+',IN'
    else:
        city=s
    unit='C'
    params = {
        'q': city,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    response = requests.get(Config.FORECAST_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        forcast=[]
        for value in data['list']:
            wf=[
                datetime.datetime.fromtimestamp(value['dt']),
                temp_convert(value['main']['temp'], unit),
                temp_convert(value['main']['feels_like'], unit),
                temp_convert(value['main']['temp_max'], unit),
                temp_convert(value['main']['temp_min'], unit),
                value['main']['humidity'],
                value['weather'][0]['description'],
                value['weather'][0]['icon']
            ]
            forcast.append(wf)
        return forcast






def get_air_pollution(s):
    if s.isnumeric():
        city=s+',IN'
    else:
        city=s
    params = {
        'q': city,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    aqi_scale={1:'Good',2:'Fair',3:'Moderate',4:'Poor',5:'Very Poor'}
    response = requests.get(Config.BASE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        lat= data['coord']['lat']
        lon= data['coord']['lon']
    params1={
        'lat': lat,
        'lon': lon,
        'appid': Config.OPENWEATHERMAP_API_KEY
    }
    response1=requests.get(Config.POLLUTION_API_URL,params1)
    if response1.status_code == 200:
        data1=response1.json()
        current_data=[
                        datetime.datetime.fromtimestamp(data1['list'][0]['dt']).date(),
                        str(data1['list'][0]['main']['aqi'])+" "+str(aqi_scale[data1['list'][0]['main']['aqi']]),
                        data1['list'][0]['components']['co'],
                        data1['list'][0]['components']['no'],
                        data1['list'][0]['components']['no2'],
                        data1['list'][0]['components']['o3'],
                        data1['list'][0]['components']['so2'],
                        data1['list'][0]['components']['pm2_5'],
                        data1['list'][0]['components']['pm10'],
                        data1['list'][0]['components']['nh3']
                    ]

    response2=requests.get(Config.POLLUTION_FORECAST_API_URL,params1)
    if response2.status_code == 200:
        data2=response2.json()         
        forcast_data=[]
        #print(data2['list'])
        for data in data2['list']:
            cd=[
                        datetime.datetime.fromtimestamp(data['dt']),
                        str(data1['list'][0]['main']['aqi'])+" "+str(aqi_scale[data1['list'][0]['main']['aqi']]),
                        data['components']['co'],
                        data['components']['no'],
                        data['components']['no2'],
                        data['components']['o3'],
                        data['components']['so2'],
                        data['components']['pm2_5'],
                        data['components']['pm10'],
                        data['components']['nh3']
                ]
            #print(cd)
            forcast_data.append(cd)
        #print(forcast_data)
    return [current_data,forcast_data]
            
            

def display_table(unit='C'):
    summaries=[]
    for city in Config.METROS:
        data=fetch_weather_data(city,unit)
        records = WeatherData.query.filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == date.today()
        ).all()
        if records:
            avg_temp = round(sum([r.temp for r in records]) / len(records),2)
            avg_temp =temp_convert(avg_temp, unit)
            dominant_weather = max(set([r.main for r in records]), key=[r.main for r in records].count)
        else:
            avg_temp=data['temp']
            dominant_weather=data['main']
        max_temp=data['max_temp']
        min_temp=data['min_temp']
        
        summary=[city,date.today(),avg_temp,max_temp,min_temp,dominant_weather,data['temp']]
        #print(summary)
        summaries.append(summary)
    return summaries
    
    

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
    data=display_table()
    for i in data:
        summary = DailyWeatherSummary(
                city=i[0],
                date=i[1],
                avg_temp=i[2],
                max_temp=i[3],
                min_temp=i[4],
                dominant_weather=i[5]
            )
        db.session.add(summary)
        db.session.commit()