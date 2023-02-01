from flask import redirect, jsonify
from src.repositories.general_database_repository import GeneralDatabaseRepository
from src.services.station_service import StationService
from src.models.station import Station
from src.models.journey import Journey


class Routes:
    def __init__(self, general_repository, station_service, journey_service, db):
        self.general_repository = general_repository
        self.station_service = station_service
        self.journey_service = journey_service
        self.db = db

    def add_routes(self, app):
        @app.route('/')
        def index():
            return 'Welcome to City Bike App!'

        @app.route('/api/database_info')
        def database_info():
            result = self.general_repository.get_database_info()
            return jsonify(result)

        @app.route('/api/station_info/<int:id>')
        def station_info(id):
            # # sql = 'SELECT S.id, S.name_fi, S.address_fi, S.x_coord, S.y_coord, \
            # #     COUNT(D.id) AS departures \
            # #     FROM station S, journey D WHERE D.departure_station=S.id \
            # #     AND S.id=:id GROUP BY S.id'
            # sql = 'SELECT S.id, S.name_fi, S.address_fi, S.x_coord, S.y_coord \
            #     FROM station S WHERE S.id=:id'
            # # TODO: Get returns
            # # TODO: Use Model
            # result = db.session.execute(sql, {'id': id})
            # station_info = result.fetchone()

            station_info = self.station_service.get_station_info(id)
            if not station_info:
                # TODO: HTTP status
                return jsonify({'Error': f'Station with id {id} not found'})
            # return jsonify({
            #     'id': station_info[0],
            #     'name_fi': station_info[1],
            #     'address_fi': station_info[2],
            #     'x_coord': station_info[3],
            #     'y_coord': station_info[4],
            #     # 'departures': station_info[5],
            # })
            return jsonify(station_info)
