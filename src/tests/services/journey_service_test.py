import unittest
from datetime import datetime

from src.repositories.database import db
from src.repositories.journey_repository import JourneyRepository
from src.services.journey_service import JourneyService
from src.models.station import Station


class MockStationRepository:
    def __init__(self) -> None:
        self.stations = {
            138: Station(138, 'Arabiankatu', 'Arabiankatu 7', 0, 0),
            541: Station(541, 'Aalto-yliopisto (M), Korkea', 'Otaniementie 10', 0, 0),
            547: Station(547, 'Jämeräntaival', 'Otakaari 18', 0, 0),
            45: Station(45, 'Brahen kenttä', 'Helsinginkatu 22', 0, 0),
            4: Station(4, 'Viiskulma', 'Fredrikinkatu 19', 0, 0),
            222: Station(222, 'Huovitie', 'Huovitie 10', 0, 0),
            95: Station(95, 'Munkkiniemen aukio', 'Munkkiniemen puistotie 1', 0, 0),
            517: Station(517, 'Länsituuli', 'Länsituulenkuja 3', 0, 0),
            9: Station(9, 'Erottajan aukio', 'Eteläesplanadi 22', 0, 0),
            40: Station(40, 'Hakaniemi (M)', 'John Stenberginranta 6', 0, 0),
            239: Station(239, 'Viikin tiedepuisto', 'Viikintori', 0, 0),
            286: Station(286, 'Mamsellimyllynkatu', 'Mamsellimyllynkatu 26', 0, 0),
            89: Station(89, 'Tilkanvierto', 'Tilkankatu 41', 0, 0),
            711: Station(711, 'Kirjurinkuja', 'Kirjurinkuja 1', 0, 0),
            113: Station(113, 'Pasilan asema', 'Pasilan asema-aukio', 0, 0),
            78: Station(78, 'Messeniuksenkatu', 'Messeniuksenkatu 1a', 0, 0),
            325: Station(325, 'Mellunmäki (M)', 'Pallaksentie 3', 0, 0),
            283: Station(283, 'Alakiventie', 'Alakiventie 4', 0, 0),
            11: Station(11, 'Unioninkatu', 'Eteläesplanadi 1', 0, 0),
            16: Station(16, 'Liisanpuistikko', 'Liisankatu 1', 0, 0),
            12: Station(12, 'Kanavaranta', 'Kanavaranta 1', 0, 0),
            30: Station(30, 'Itämerentori', 'Itämerentori 1', 0, 0),
            10: Station(10, 'Kasarmitori', 'Fabianinkatu 13', 0, 0),
        }

    def get_station(self, id: int):
        if id not in self.stations:
            raise ValueError
        return self.stations[id]


class TestJourneyService(unittest.TestCase):
    def setUp(self):
        journey_repository = JourneyRepository(db)
        mock_station_repository = MockStationRepository()
        self.service_with_mock_stations = JourneyService(
            journey_repository, mock_station_repository
        )

    def test_parses_valid_string(self):
        result = self.service_with_mock_stations.parse_journey(
            [
                '2021-05-01T00:00:11', '2021-05-01T00:04:34', '138', 'Arabiankatu',
                '138', 'Arabiankatu', '1057', '259'
            ]
        )

        self.assertEqual(result.departure_time,
                         datetime.fromisoformat('2021-05-01T00:00:11'))
        self.assertEqual(result.return_time,
                         datetime.fromisoformat('2021-05-01T00:04:34'))
        self.assertEqual(result.departure_station, 138)
        self.assertEqual(result.return_station, 138)
        self.assertEqual(result.distance, 1057)
        self.assertEqual(result.duration, 259)

    def test_parses_valid_string_with_comma_as_part_of_the_name(self):
        result = self.service_with_mock_stations.parse_journey(
            [
                '2021-05-31T21:48:34', '2021-05-31T21:52:05', '541',
                'Aalto-yliopisto (M), Korkeakouluaukio', '547', 'Jämeräntaival',
                '702', '210'
            ]
        )

        self.assertEqual(result.departure_time,
                         datetime.fromisoformat('2021-05-31T21:48:34'))
        self.assertEqual(result.return_time,
                         datetime.fromisoformat('2021-05-31T21:52:05'))
        self.assertEqual(result.departure_station, 541)
        self.assertEqual(result.return_station, 547)
        self.assertEqual(result.distance, 702)
        self.assertEqual(result.duration, 210)

    def test_reads_and_parses_test_file_with_valid_journeys(self):
        result = self.service_with_mock_stations.parse_csv(
            './src/tests/data/journey_test.csv')

        self.assertEqual(len(result), 8)
        self.assertEqual(
            str(result[0]), '2021-05-31 20:47:12 045 -> 004 2021-05-31 21:05:56, 4149 m, 1118 sec')
        self.assertEqual(
            str(result[1]), '2021-05-31 20:45:46 222 -> 095 2021-05-31 20:56:55, 3171 m, 665 sec')
        self.assertEqual(
            str(result[2]), '2021-05-31 20:41:56 541 -> 517 2021-05-31 21:08:56, 2360 m, 1614 sec')
        self.assertEqual(
            str(result[3]), '2021-06-30 23:59:34 009 -> 040 2021-07-01 00:06:23, 1602 m, 405 sec')
        self.assertEqual(
            str(result[4]), '2021-06-30 23:39:30 239 -> 286 2021-07-01 00:05:04, 3608 m, 1529 sec')
        self.assertEqual(
            str(result[5]), '2021-06-01 00:00:01 089 -> 711 2021-06-01 00:26:27, 5660 m, 1583 sec')
        self.assertEqual(
            str(result[6]), '2021-07-31 23:59:59 113 -> 078 2021-08-01 00:09:15, 1602 m, 553 sec')
        self.assertEqual(
            str(result[7]), '2021-07-31 23:51:08 325 -> 283 2021-08-01 00:06:13, 3389 m, 900 sec')

    def test_reads_and_parses_test_file_with_some_invalid_journeys(self):
        result = self.service_with_mock_stations.parse_csv(
            './src/tests/data/invalid_journeys_test.csv')
        # TODO: Test with non-existing station

        self.assertEqual(len(result), 3)
        self.assertEqual(
            str(result[0]), '2021-05-31 20:47:12 045 -> 004 2021-05-31 21:05:56, 4149 m, 1118 sec')
        self.assertEqual(
            str(result[1]), '2021-06-01 00:00:01 089 -> 711 2021-06-01 00:26:27, 5660 m, 1583 sec')
        self.assertEqual(
            str(result[2]), '2021-07-10 23:04:17 030 -> 010 2021-07-10 23:29:15, 2983 m, 1493 sec')
