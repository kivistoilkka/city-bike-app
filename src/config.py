from os import getenv


class ProductionConfig:
    def __init__(self) -> None:
        self.database_uri = getenv('DATABASE_URL')
        self.station_file = './data/Helsingin_ja_Espoon_kaupunkipy%C3%B6r%C3%A4asemat_avoin.csv'
        self.journey_files = [
            './data/2021-05.csv',
            './data/2021-06.csv',
            './data/2021-07.csv'
        ]


class TestConfig:
    def __init__(self) -> None:
        self.database_uri = getenv("TEST_DATABASE_URL")
        self.station_file = './src/tests/data/station_test_large.csv'
        self.journey_files = ['./src/tests/data/journey_test_large.csv']
