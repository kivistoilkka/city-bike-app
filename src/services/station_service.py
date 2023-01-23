import csv
from entities.station import Station


class StationService:
    def __init__(self) -> None:
        pass

    def parse_csv(self, file) -> list:
        stations = []
        with open(file, encoding='utf-8') as csv_file:
            for line in csv.reader(csv_file, quotechar='"', delimiter=','):
                if line[0] == 'FID':
                    continue
                station = self.parse_station(line)
                stations.append(station)
        return stations

    @staticmethod
    def parse_station(line: list) -> Station:
        station_id = line[1]
        name_fi, name_sv, name_en = line[2:5]
        address_fi, address_sv = line[5:7]
        city_fi = line[7] if line[7] != ' ' else 'Helsinki'
        city_sv = line[8] if line[8] != ' ' else 'Helsingfors'
        operator = line[9] if line[9] != ' ' else ''
        capacity = int(line[10])
        x_coord = float(line[11])
        y_coord = float(line[12])

        return Station(
            station_id, name_fi, name_sv, name_en,
            address_fi, address_sv,
            city_fi, city_sv, operator, capacity,
            x_coord, y_coord
        )
