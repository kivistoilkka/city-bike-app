from os import getenv

from src.config.config import ProductionConfig, TestConfig
from src.repositories.database import db

from src.services.station_service import StationService
from src.services.journey_service import JourneyService


class DatabaseBuilder:
    def __init__(self) -> None:
        pass

    def _read_stations_and_add_to_database(self, station_service: StationService, file):
        stations = station_service.parse_csv(file)
        for station in stations:
            print(station)
            db.session.add(station)
        db.session.commit()

    def _read_journeys_and_add_to_database(self, journey_service: JourneyService, file):
        #TODO: Make an option to optimize journey parsing so that instead of returning dictionary,
        # it validates and checks journey for duplicates and adds it directly to database if ok
        print(f'Reading journeys from file {file}')
        journeys = journey_service.parse_csv(file, logs=True)
        print()
        print(f'Adding journeys from {file} to the database')
        for journey in journeys.values():
            db.session.add(journey)
            print(journey)
        db.session.commit()

    def build_database(
        self,
        stations_created: bool,
        station_service,
        journeys_created: bool,
        journey_service,
        testing: bool,
    ):
        db.create_all()
        if not stations_created:
            print('**************')
            print('Adding stations to database')
            print('**************')
            if testing or getenv('RUNNING_DEV'):
                self._read_stations_and_add_to_database(
                    station_service,
                    TestConfig().station_file
                )
            else:
                self._read_stations_and_add_to_database(
                    station_service,
                    ProductionConfig().station_file
                )
        print()
        if not journeys_created:
            print('**************')
            print('Adding journeys to database')
            print('**************')
            if testing or getenv('RUNNING_DEV'):
                for file in TestConfig().journey_files:
                    self._read_journeys_and_add_to_database(
                        journey_service,
                        file
                    )
            else:
                for file in ProductionConfig().journey_files:
                    self._read_journeys_and_add_to_database(
                        journey_service, file)
        print()
