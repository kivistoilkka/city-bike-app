from services.station_service import StationService


class App:
    def __init__(self) -> None:
        pass

    def run(self):
        station_service = StationService()
        stations = station_service.parse_csv(
            './src/tests/data/station_test.csv')
