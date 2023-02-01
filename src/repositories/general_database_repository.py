from src.models.station import Station
from src.models.journey import Journey


class GeneralDatabaseRepository:
    def get_database_info(self):
        station_count = Station.query.count()
        journey_count = Journey.query.count()
        return {
            'station_count': station_count,
            'journey_count': journey_count
        }
