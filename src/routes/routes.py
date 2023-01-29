from flask import redirect, jsonify
from src.models.station import Station
from src.models.journey import Journey

class Routes:
    def __init__(self):
        pass

    @staticmethod
    def add_routes(app, db):
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
            # sql = 'SELECT S.id, S.name_fi, S.address_fi, S.x_coord, S.y_coord, \
            #     COUNT(D.id) AS departures \
            #     FROM station S, journey D WHERE D.departure_station=S.id \
            #     AND S.id=:id GROUP BY S.id'
            sql = 'SELECT S.id, S.name_fi, S.address_fi, S.x_coord, S.y_coord \
                FROM station S WHERE S.id=:id'
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
                #'departures': station_info[5],
            })
