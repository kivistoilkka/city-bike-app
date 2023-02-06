from os import getenv

from src.config.config import ProductionConfig, TestConfig
from src.repositories.database import db

from src.models.station import Station
from src.models.journey import Journey

from src.services.station_service import StationService
from src.services.journey_service import JourneyService


class DatabaseBuilder:
    def __init__(self) -> None:
        pass

    def _read_stations_and_add_to_database(self, station_service: StationService, file:str) -> dict:
        stations = station_service.parse_csv(file)
        for station in stations.values():
            print(station)
            db.session.add(station)
        db.session.commit()
        return stations

    def _read_journeys_and_add_to_database(
        self,journey_service: JourneyService, file:str, stations:dict, optimized:bool
    ):
        if optimized:
            print(f'Reading and adding journeys from file {file}')
        else:
            print(f'Reading journeys from file {file}')
        journeys = journey_service.parse_csv(file, stations, optimized, logs=True)
        if optimized:
            return
        print()
        print(f'Adding journeys from {file} to the database')
        for journey in journeys.values():
            db.session.add(journey)
            print('Added:', journey)
        db.session.commit()

    def build_database(
        self,
        stations_created: bool,
        station_service,
        journeys_created: bool,
        journey_service,
        testing: bool,
        optimized: bool
    ):
        if not stations_created:
            Station.__table__.create(db.engine)
            print('**************')
            print('Adding stations to database')
            print('**************')
            if testing or getenv('RUNNING_DEV'):
                stations = self._read_stations_and_add_to_database(
                    station_service,
                    TestConfig().station_file
                )
            else:
                stations = self._read_stations_and_add_to_database(
                    station_service,
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
                        file,
                        stations,
                        optimized
                    )
            else:
                for file in ProductionConfig().journey_files:
                    self._read_journeys_and_add_to_database(
                        journey_service, file, stations, optimized)
        print()
