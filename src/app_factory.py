from os import getenv
from flask import Flask
from sqlalchemy import inspect

from src.config import ProductionConfig, TestConfig
from src.repositories.database import db
from src.database_builder import DatabaseBuilder

from src.services.station_service import StationService
from src.services.journey_service import JourneyService
from src.routes.routes import Routes


class AppFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_app(testing=False) -> Flask:
        app = Flask(__name__)
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        uri = ProductionConfig().database_uri
        if testing or getenv('RUNNING_DEV'):
            uri = TestConfig().database_uri
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

        db.init_app(app)

        station_service = StationService(db)
        journey_service = JourneyService(station_service)
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

        Routes().add_routes(app, db)

        return app
