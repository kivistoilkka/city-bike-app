from flask import jsonify, abort, render_template, redirect
from sqlalchemy.exc import SQLAlchemyError


class Routes:
    def __init__(self, general_repository, station_service, journey_service):
        self.general_repository = general_repository
        self.station_service = station_service
        self.journey_service = journey_service

    def add_routes(self, app):
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/stations')
        def front_stations():
            return redirect('/')

        @app.route('/journeys')
        def front_journeys():
            return redirect('/')

        @app.route('/stations/<int:id>')
        def front_station_info(id):
            return redirect('/')

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

        @app.route('/api/all_stations_id_decreasing/')
        def all_stations_id_decreasing():
            try:
                station_list = self.station_service.get_all_stations_in_decreasing_id_order()
                return jsonify(station_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))

        @app.route('/api/stations_id_decreasing/<int:lower>_<int:upper>')
        def stations_id_decreasing(lower, upper):
            if upper < lower:
                return abort(404, 'Upper limit cannot be smaller than lower limit')
            try:
                station_list = self.station_service.get_stations_in_decreasing_id_order(
                    lower, upper
                )
                return jsonify(station_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))

        @app.route('/api/journeys_time_decreasing/<int:lower>_<int:upper>')
        def journeys_time_decreasing(lower, upper):
            if upper < lower:
                return abort(404, 'Upper limit cannot be smaller than lower limit')
            try:
                journey_list = self.journey_service.get_journeys_in_decreasing_time_order(
                    lower, upper
                )
                return jsonify(journey_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))

        @app.route('/api/journeys_time_increasing/<int:lower>_<int:upper>')
        def journeys_time_increasing(lower, upper):
            if upper < lower:
                return abort(404, 'Upper limit cannot be smaller than lower limit')
            try:
                journey_list = self.journey_service.get_journeys_in_increasing_time_order(
                    lower, upper
                )
                return jsonify(journey_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))

        @app.route('/api/journeys_distance/<int:lower>_<int:upper>')
        def journeys_distance(lower, upper):
            if upper < lower:
                return abort(404, 'Upper limit cannot be smaller than lower limit')
            try:
                journey_list = self.journey_service.get_journeys_in_distance_order(
                    lower, upper
                )
                return jsonify(journey_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))

        @app.route('/api/journeys_duration/<int:lower>_<int:upper>')
        def journeys_duration(lower, upper):
            if upper < lower:
                return abort(404, 'Upper limit cannot be smaller than lower limit')
            try:
                journey_list = self.journey_service.get_journeys_in_duration_order(
                    lower, upper
                )
                return jsonify(journey_list)
            except ValueError as err:
                return abort(404, str(err))
            except SQLAlchemyError as err:
                return abort(404, str(err))
