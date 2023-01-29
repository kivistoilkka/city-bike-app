from src.models.station import Station


class StationRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_station(self, id: int) -> Station:
        station = Station.query.filter_by(id=id).first()
        if not station:
            raise ValueError('Station id not in database')
        return station
