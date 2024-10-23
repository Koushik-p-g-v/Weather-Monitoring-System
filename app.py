from flask import Flask, render_template, request, redirect, url_for
from models import db  # Import only necessary components from models
from config import Config
from process import display_table
import threading
import time
from process import fetch_weather_data, store_weather_data, rollup_daily_summaries, search_city_summaries, get_air_pollution, get_weather_forecast

app = Flask(__name__)
alert_cities=[]
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
db.init_app(app)


@app.route('/')
def index():
    # Fetch the daily summaries from the database
    unit = request.args.get('unit', 'C')
    summaries = display_table(unit)
    global alert_cities
    current_alerts = alert_cities[:]
    alert_cities.clear()  # Clear the list once the alerts have been shown
    return render_template('index.html', summaries=summaries, alerts=current_alerts)


@app.route('/search')
def search():
    query = request.args.get('query', '')
    search_results = search_city_summaries(query)  # Assume search functionality is implemented
    return render_template('search.html', query=query, result=search_results)

@app.route('/addcity', methods=['POST'])
def add_city():
    city_name = request.form.get('cityName')
    if city_name and city_name not in Config.METROS:
        Config.METROS.append(city_name)
    return redirect(url_for('index'))

@app.route('/removecity', methods=['POST'])
def remove_city():
    city_name = request.form.get('removeCityName')
    if city_name in Config.METROS:
        Config.METROS.remove(city_name)
    return redirect(url_for('index'))

@app.route('/forecast', methods=['GET'])
def forecast():
    city = request.args.get('city', '')  # Get the city name from the search bar
    forecast_data = None

    if city:  # Only fetch forecast data if a city is entered
        forecast_data_raw = get_weather_forecast(city)
        if forecast_data_raw:
            forecast_data={}
            for data in forecast_data_raw:
                forecast_date = data[0].date()
                if forecast_date not in forecast_data:
                    forecast_data[forecast_date] = []
                forecast_data[forecast_date].append(data)
            forecast_data = list(forecast_data.values())
            #print(forecast_data)
    return render_template('forecast.html', city=city, forecast_data=forecast_data)



@app.route('/air-pollution', methods=['GET', 'POST'])
def air_pollution():
    city = request.args.get('city', '')  # Get city from the search bar, default to an empty string
    pollution_data = None

    if city:  # Only fetch pollution data if a city is entered
        pollution_data = get_air_pollution(city)
        if pollution_data:
            current_data, forecast_data_raw = pollution_data[0], pollution_data[1]
            forecast_data = {}
            for data in forecast_data_raw:
                forecast_date = data[0].date()
                if forecast_date not in forecast_data:
                    forecast_data[forecast_date] = []
                forecast_data[forecast_date].append(data)
            forecast_data = list(forecast_data.values())
        else:
            current_data, forecast_data = [], []
    else:
        current_data, forecast_data = None, None
    #print(forecast_data)

    return render_template('airpollution.html', city=city, current_data=current_data, forecast_data=forecast_data)


@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    threshold = float(request.form.get('threshold'))
    Config.ALERT_THRESHOLD_TEMP=threshold
    return redirect(url_for('index'))

def get_alert(city):
    global alert_cities
    alert_cities.append(city)

def start_weather_monitoring():
    with app.app_context():  # This ensures the background thread has access to the Flask app context
        last_weather_time = time.time()
        last_rollup_time = time.time()
        violation_cities=[]
        while True:
            current_time = time.time()
            if current_time - last_weather_time >= Config.INTERVAL:
                for city in Config.METROS:
                    weather_data = fetch_weather_data(city)
                    if weather_data:
                        if weather_data['violation']:
                            violation_cities.append(city)
                            if(city in Config.CITY_THRESHOLD):
                                get_alert(city)
                        store_weather_data(weather_data)
                last_weather_time = current_time  # Update time of last weather data fetch
                Config.CITY_THRESHOLD= violation_cities
            # Roll up daily summaries every DAY_INTERVAL seconds
            if current_time - last_rollup_time >= Config.DAY_INTERVAL:
                rollup_daily_summaries()
                last_rollup_time = current_time  # Update time of last rollup

            time.sleep(1) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if not exists
        monitoring_thread = threading.Thread(target=start_weather_monitoring)
        monitoring_thread.start()
    app.run(debug=True)
