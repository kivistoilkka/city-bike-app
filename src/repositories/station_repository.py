from src.models.station import Station


class StationRepository:
    def __init__(self, db) -> None:
        pass  # self.db = db

    def get_station(self, id: int) -> Station:
        station = Station.query.filter_by(id=id).first()
        if not station:
            raise ValueError('Station id not in database')
        return station

    def get_all_stations(self) -> list:
        stations = Station.query.order_by(Station.id).all()
        return stations

    def get_range_from_all_stations(self, lower: int, upper: int) -> list:
        """Returns sublist of stations from ordered list of all stations, including
        station in position lower of the list (counting starts from 0) and excluding
        station in position upper.

        Args:
            lower (int): First position to be included, counting starts from 0
            upper (int): Position after the last to be included

        Returns:
            list: List of Station objects in numerical order by id
        """
        stations = Station.query.order_by(Station.id).limit(
            upper-lower).offset(lower).all()
        return stations
