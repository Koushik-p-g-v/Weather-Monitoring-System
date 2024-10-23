class Config:
    OPENWEATHERMAP_API_KEY = '5c20a1c3b6f4a39c8accd846632d75ea'
    BASE_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
    POLLUTION_API_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'
    POLLUTION_FORECAST_API_URL = 'http://api.openweathermap.org/data/2.5/air_pollution/forecast'
    FORECAST_API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
    METROS = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad','Ahmedabad','Pune','Surat','Vijayawada','Eluru']
    CITY_THRESHOLD=[]
    METRO_DICT = {metro: 0 for metro in METROS}
    INTERVAL = 300  # API call interval in seconds (5 minutes)
    DAY_INTERVAL = 86399
    ALERT_THRESHOLD_TEMP = 35  # Celsius
    DATABASE_URI = 'sqlite:///weather_data.db'  # Local SQLite DB path
