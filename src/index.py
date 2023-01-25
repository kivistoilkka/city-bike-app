from os import getenv
from flask import Flask, redirect, jsonify

from src.repositories.database import db

from src.models.station import Station
from src.models.journey import Journey

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL") #.replace("://", "ql://", 1)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    result = db.session.execute('SELECT COUNT(*) FROM stations')
    count = result.fetchone()
    return f'Stations in database: {count[0]}'

@app.route('/api/database_info')
def database_info():
    result = db.session.execute('SELECT COUNT(*) FROM stations')
    station_count = result.fetchone()[0]
    result = db.session.execute('SELECT COUNT(*) FROM journeys')
    journey_count = result.fetchone()[0]
    return jsonify({
        'station_count': station_count,
        'journey_count': journey_count
    })

@app.route('/add_station')
def add_station():
    sql = 'INSERT INTO stations (id,name_fi,address_fi,x_coord,y_coord) VALUES (:id,:name_fi,:address_fi,:x_coord,:y_coord)'
    db.session.execute(sql, {'id':1, 'name_fi':"Kaivopuisto", 'address_fi':"Meritori 1", 'x_coord':24.9502114714031, 'y_coord':60.155369615074})
    db.session.commit()
    new_station = Station(405, 'Jollas', 'Jollaksentie 33', 25.0616678668253,60.1644074899774)
    db.session.add(new_station)
    db.session.commit()
    return redirect('/')
