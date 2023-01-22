from entities.station import Station


class StationService:
    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_station(text: str) -> Station:
        parts = text.split(',')
        station_id = int(parts[1])
        name_fi, name_sv, name_en = parts[2:5]
        address_fi, address_sv, city_fi, city_sv = parts[5:9]
        operator = parts[9]
        capacity = int(parts[10])
        x_coord = float(parts[11])
        y_coord = float(parts[12])

        return Station(
            station_id, name_fi, name_sv, name_en,
            address_fi, address_sv,
            city_fi, city_sv, operator, capacity,
            x_coord, y_coord
        )
