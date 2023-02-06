from os import getenv
from sqlalchemy.orm import sessionmaker

from src.config.config import ProductionConfig, TestConfig
from src.repositories.database import db

from src.models.station import Station
from src.models.journey import Journey

from src.services.station_service import StationService
from src.services.journey_service import JourneyService


class DatabaseBuilder:
    def __init__(self) -> None:
        pass

    def _read_stations_and_add_to_database(
        self, station_service: StationService, session, file: str
    ) -> dict:
        stations = station_service.parse_csv(file)
        session.add_all(stations.values())
        session.commit()
        return stations

    def _read_journeys_and_add_to_database(
        self, journey_service: JourneyService, session, file: str, stations: dict
    ):
        print(f'Reading journeys from file {file}')
        journeys = journey_service.parse_csv(file, stations, logs=False)

        print()
        print(f'Adding journeys from {file} to the database')
        session.add_all(journeys.values())
        session.commit()

    def build_database(
        self,
        stations_created: bool,
        station_service,
        journeys_created: bool,
        journey_service,
        testing: bool
    ):
        session_maker = sessionmaker()
        session_maker.configure(bind=db.engine)
        session = session_maker()
        if not stations_created:
            Station.__table__.create(db.engine)
            print('**************')
            print('Adding stations to database')
            print('**************')
            if testing or getenv('RUNNING_DEV'):
                stations = self._read_stations_and_add_to_database(
                    station_service,
                    session,
                    TestConfig().station_file
                )
            else:
                stations = self._read_stations_and_add_to_database(
                    station_service,
                    session,
                    ProductionConfig().station_file
                )
        print()
        if not journeys_created:
            Journey.__table__.create(db.engine)
            print('**************')
            print('Adding journeys to database')
            print('**************')
            if not stations:
                station_list = station_service.get_all_stations_in_decreasing_id_order()
                stations = {}
                for station in station_list:
                    stations[station.id] = station
            if testing or getenv('RUNNING_DEV'):
                for file in TestConfig().journey_files:
                    self._read_journeys_and_add_to_database(
                        journey_service,
                        session,
                        file,
                        stations
                    )
            else:
                for file in ProductionConfig().journey_files:
                    self._read_journeys_and_add_to_database(
                        journey_service, session, file, stations)
        print()
