from config import Config

def add_City(city):
    Config.METROS.append(city)

def search_City(s):
    if s.isnum():
        city=s+',IN'
    else:
        city=s
    fetch_weather_data(city)
    #convert into different units
    #alerts
    #display in new html file
    #add avg-humidity,avg-pressure feature 
    #add login page