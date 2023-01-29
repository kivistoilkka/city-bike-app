from os import getenv
from flask import Flask, redirect, jsonify
from sqlalchemy import inspect

from src.repositories.database import db

from src.models.station import Station
from src.models.journey import Journey

from src.services.station_service import StationService
from src.services.journey_service import JourneyService

def read_stations_and_add_to_database(station_service:StationService, file):
    stations = station_service.parse_csv(file)
    for station in stations:
        print(station)
        db.session.add(station)
    db.session.commit()

def read_journeys_and_add_to_database(journey_service:JourneyService, file):
    print(f'Reading joyrneys from file {file}')
    journeys = journey_service.parse_csv(file,logs=True)
    print(f'Adding journeys from {file} to the database')
    for journey in journeys:
        db.session.add(journey)
        print(journey)
    db.session.commit()

def build_database(
    stations_created,
    station_service,
    journeys_created,
    journey_service,
    testing,
):
    db.create_all()
    if not stations_created:
        print('**************')
        print('Adding stations to database')
        print('**************')
        if testing:
            read_stations_and_add_to_database(
                station_service,
                './src/tests/data/station_test_large.csv'
            )
        else:
            read_stations_and_add_to_database(
                station_service,
                './data/Helsingin_ja_Espoon_kaupunkipy%C3%B6r%C3%A4asemat_avoin.csv'
            )
        print()
    if not journeys_created:
        print('**************')
        print('Adding journeys to database')
        print('**************')
        if testing:
            read_journeys_and_add_to_database(
                journey_service,
                './src/tests/data/journey_test_large.csv'
            )
        else:
            read_journeys_and_add_to_database(journey_service, './data/2021-05.csv')
        print('')

def create_app(testing=False) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    uri = getenv("DATABASE_URL")
    if testing:
        uri = getenv("TEST_DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    db.init_app(app)

    station_service = StationService(db)
    journey_service = JourneyService(station_service)

    with app.app_context():
        # db.drop_all() ######################################
        inspector = inspect(db.engine)
        stations_created = inspector.has_table('station')
        journeys_created = inspector.has_table('journey')
        if not stations_created or not journeys_created:
            build_database(
                stations_created,
                station_service,
                journeys_created,
                journey_service,
                testing
            )

    @app.route('/')
    def index():
        result = db.session.execute('SELECT COUNT(*) FROM station')
        count = result.fetchone()
        return f'Stations in database: {count[0]}'

    @app.route('/api/database_info')
    def database_info():
        result = db.session.execute('SELECT COUNT(*) FROM station')
        station_count = result.fetchone()[0]
        result = db.session.execute('SELECT COUNT(*) FROM journey')
        journey_count = result.fetchone()[0]
        return jsonify({
            'station_count': station_count,
            'journey_count': journey_count
        })

    @app.route('/add_station')
    def add_station():
        sql = 'INSERT INTO station (id,name_fi,address_fi,x_coord,y_coord) \
            VALUES (:id,:name_fi,:address_fi,:x_coord,:y_coord)'
        db.session.execute(sql, {'id': 1, 'name_fi': "Kaivopuisto", 'address_fi': "Meritori 1",
                           'x_coord': 24.9502114714031, 'y_coord': 60.155369615074})
        db.session.commit()
        new_station = Station(405, 'Jollas', 'Jollaksentie 33',
                              25.0616678668253, 60.1644074899774)
        db.session.add(new_station)
        db.session.commit()
        return redirect('/')

    @app.route('/api/station_info/<int:id>')
    def station_info(id):
        sql = 'SELECT S.id, S.name_fi, S.address_fi, S.x_coord, S.y_coord, \
            COUNT(D.id) AS departures \
            FROM station S, journey D WHERE D.departure_station=S.id \
            AND S.id=:id GROUP BY S.id'
        #TODO: Get returns
        #TODO: Use Model
        result = db.session.execute(sql, {'id': id})
        station_info = result.fetchone()
        if not station_info:
            return jsonify({'Error': f'Station with id {id} not found'})  #TODO: HTTP status
        return jsonify({
            'id': station_info[0],
            'name_fi': station_info[1],
            'address_fi': station_info[2],
            'x_coord': station_info[3],
            'y_coord': station_info[4],
            'departures': station_info[5],
        })

    return app


if __name__ == '__main__':
    application = create_app()
    application.run()
