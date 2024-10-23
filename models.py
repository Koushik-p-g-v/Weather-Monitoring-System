from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    main = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.Date, nullable=False)

class DailyWeatherSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    dominant_weather = db.Column(db.String(50), nullable=False)
