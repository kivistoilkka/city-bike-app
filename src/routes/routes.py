from flask import redirect, jsonify, abort
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
            try:
                station_info = self.station_service.get_station_info(id)
                return jsonify(station_info)
            except ValueError as err:
                return abort(404, str(err))
