from os import getenv
from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect

from src.config.config import ProductionConfig, TestConfig
from src.repositories.database import db
from src.database_builder import DatabaseBuilder

from src.repositories.general_database_repository import GeneralDatabaseRepository
from src.repositories.station_repository import StationRepository
from src.repositories.journey_repository import JourneyRepository

from src.services.station_service import StationService
from src.services.journey_service import JourneyService
from src.routes.routes import Routes


class AppFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_app(testing=False) -> Flask:
        app = Flask(
            __name__,
            static_folder='../build', template_folder='../build',
            static_url_path='/'
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        if testing or getenv('RUNNING_DEV'):
            uri = TestConfig().database_uri
        else:
            uri = ProductionConfig().database_uri
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

        db.init_app(app)

        general_repository = GeneralDatabaseRepository()
        station_repository = StationRepository(db)
        journey_repository = JourneyRepository(db)

        station_service = StationService(db, station_repository)
        journey_service = JourneyService(
            journey_repository, station_repository)

        database_builder = DatabaseBuilder()
        with app.app_context():
            if testing or getenv('RUNNING_DEV') or getenv('BUILD_PROD_DB'):
                db.drop_all()
            inspector = inspect(db.engine)
            stations_created = inspector.has_table('station')
            journeys_created = inspector.has_table('journey')
            if not stations_created or not journeys_created:
                database_builder.build_database(
                    stations_created,
                    station_service,
                    journeys_created,
                    journey_service,
                    testing
                )

        CORS(app)
        Routes(
            general_repository,
            station_service,
            journey_service
        ).add_routes(app)

        return app
