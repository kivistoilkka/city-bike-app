import csv
from src.models.station import Station


class StationService:
    def __init__(self, db, station_repository) -> None:
        self.db = db
        self.station_repository = station_repository

    def parse_csv(self, file) -> list:
        stations = []
        with open(file, encoding='utf-8') as csv_file:
            for line in csv.reader(csv_file, quotechar='"', delimiter=','):
                if line[0] == 'FID':
                    continue
                try:
                    station = self.parse_station(line)
                    stations.append(station)
                except ValueError:
                    continue
        return stations

    def validate_station(self, station: Station) -> bool:
        if station.x_coord < 19 or station.x_coord > 32:
            return False
        if station.y_coord < 59 or station.y_coord > 71:
            return False
        return True

    def parse_station(self, line: list) -> Station:
        station_id = int(line[1])
        name_fi = line[2]
        address_fi = line[5]
        x_coord = float(line[11])
        y_coord = float(line[12])

        station = Station(
            station_id, name_fi, address_fi, x_coord, y_coord
        )

        validation_result = self.validate_station(station)
        if not validation_result:
            raise ValueError
        return station

    def get_station_info(self, id: int) -> Station:
        station = self.station_repository.get_station(id)
        if not station:
            return None
        return {
            'id': station.id,
            'name_fi': station.name_fi,
            'address_fi': station.address_fi,
            'x_coord': station.x_coord,
            'y_coord': station.y_coord,
        }
