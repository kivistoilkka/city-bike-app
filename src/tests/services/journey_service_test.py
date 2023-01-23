import unittest
from datetime import datetime
from services.journey_service import JourneyService


class TestJourneyService(unittest.TestCase):
    def setUp(self):
        self.service = JourneyService()

    def test_parses_valid_string(self):
        result = self.service.parse_journey(
            [
                '2021-05-01T00:00:11', '2021-05-01T00:04:34', '138', 'Arabiankatu',
                '138', 'Arabiankatu', '1057', '259'
            ]
        )

        self.assertEqual(result.departure_time,
                         datetime.fromisoformat('2021-05-01T00:00:11'))
        self.assertEqual(result.return_time,
                         datetime.fromisoformat('2021-05-01T00:04:34'))
        self.assertEqual(result.departure_station_id, '138')
        self.assertEqual(result.departure_station_name, 'Arabiankatu')
        self.assertEqual(result.return_station_id, '138')
        self.assertEqual(result.return_station_name, 'Arabiankatu')
        self.assertEqual(result.distance, 1057)
        self.assertEqual(result.duration, 259)

    def test_parses_valid_string_with_comma_as_part_of_the_name(self):
        result = self.service.parse_journey(
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
        self.assertEqual(result.departure_station_id, '541')
        self.assertEqual(result.departure_station_name,
                         'Aalto-yliopisto (M), Korkeakouluaukio')
        self.assertEqual(result.return_station_id, '547')
        self.assertEqual(result.return_station_name, 'Jämeräntaival')
        self.assertEqual(result.distance, 702)
        self.assertEqual(result.duration, 210)

    def test_reads_and_parses_test_file_with_valid_journeys(self):
        result = self.service.parse_csv('./src/tests/data/journey_test.csv')

        self.assertEqual(len(result), 8)
        self.assertEqual(
            str(result[0]), '045 Brahen kenttä -> 004 Viiskulma, 4149 m, 1118 sec')
        self.assertEqual(
            str(result[1]), '222 Huovitie -> 095 Munkkiniemen aukio, 3171 m, 665 sec')
        self.assertEqual(
            str(result[2]), '541 Aalto-yliopisto (M), Korkeakouluaukio -> 517 Länsituuli, 2360 m, 1614 sec')
        self.assertEqual(
            str(result[3]), '009 Erottajan aukio -> 040 Hakaniemi (M), 1602 m, 405 sec')
        self.assertEqual(
            str(result[4]), '239 Viikin tiedepuisto -> 286 Mamsellimyllynkatu, 3608 m, 1529 sec')
        self.assertEqual(
            str(result[5]), '089 Tilkanvierto -> 711 Kirjurinkuja, 5660 m, 1583 sec')
        self.assertEqual(
            str(result[6]), '113 Pasilan asema -> 078 Messeniuksenkatu, 1602 m, 553 sec')
        self.assertEqual(
            str(result[7]), '325 Mellunmäki (M) -> 283 Alakiventie, 3389 m, 900 sec')

    def test_reads_and_parses_test_file_with_some_invalid_journeys(self):
        result = self.service.parse_csv(
            './src/tests/data/invalid_journeys_test.csv')

        self.assertEqual(len(result), 3)
        self.assertEqual(
            str(result[0]), '045 Brahen kenttä -> 004 Viiskulma, 4149 m, 1118 sec')
        self.assertEqual(
            str(result[1]), '089 Tilkanvierto -> 711 Kirjurinkuja, 5660 m, 1583 sec')
        self.assertEqual(
            str(result[2]), '030 Itämerentori -> 010 Kasarmitori, 2983 m, 1493 sec')
