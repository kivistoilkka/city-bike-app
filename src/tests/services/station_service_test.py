import unittest
from src.services.station_service import StationService


class TestStationService(unittest.TestCase):
    def setUp(self):
        self.service = StationService()

    def test_parses_valid_line(self):
        result = self.service.parse_station(
            [
                '1', '501', 'Hanasaari', 'Hanaholmen', 'Hanasaari', 'Hanasaarenranta 1',
                'Hanaholmsstranden 1', 'Espoo', 'Esbo', 'CityBike Finland', '10',
                '24.840319', '60.16582'
            ]
        )

        self.assertEqual(result.id, 501)
        self.assertEqual(result.name_fi, 'Hanasaari')
        self.assertEqual(result.address_fi, 'Hanasaarenranta 1')
        self.assertEqual(result.x_coord, 24.840319)
        self.assertEqual(result.y_coord, 60.16582)

    def test_parses_valid_line_with_comma_as_part_of_the_name(self):
        result = self.service.parse_station(
            [
                '22', '539', 'Aalto-yliopisto (M), Tietot', 'Aalto-universitetet (M),',
                'Aalto University (M), Tietotie', 'Tietotie 4', 'Datavägen 4', 'Espoo',
                'Esbo', 'CityBike Finland', '20', '24.820099', '60.184987'
            ]
        )
        self.assertEqual(result.id, 539)
        self.assertEqual(result.name_fi, 'Aalto-yliopisto (M), Tietot')
        self.assertEqual(result.address_fi, 'Tietotie 4')
        self.assertEqual(result.x_coord, 24.820099)
        self.assertEqual(result.y_coord, 60.184987)

    def test_parses_valid_string_for_station_in_Helsinki(self):
        result = self.service.parse_station(
            [
                '111', '001', 'Kaivopuisto', 'Brunnsparken', 'Kaivopuisto', 'Meritori 1',
                'Havstorget 1', ' ', ' ', ' ', '30', '24.9502114714031', '60.155369615074'
            ]
        )

        self.assertEqual(result.id, 1)
        self.assertEqual(result.name_fi, 'Kaivopuisto')
        self.assertEqual(result.address_fi, 'Meritori 1')
        self.assertEqual(result.x_coord, 24.9502114714031)
        self.assertEqual(result.y_coord, 60.155369615074)

    def test_reads_and_parses_test_file_with_valid_stations(self):
        result = self.service.parse_csv('./src/tests/data/station_test.csv')

        self.assertEqual(len(result), 7)
        self.assertEqual(
            str(result[0]), '501 Hanasaari: Hanasaarenranta 1, x=24.840319, y=60.16582')
        self.assertEqual(str(
            result[1]), '539 Aalto-yliopisto (M), Tietot: Tietotie 4, x=24.820099, y=60.184987')
        self.assertEqual(str(
            result[2]), '541 Aalto-yliopisto (M), Korkea: Otaniementie 10, x=24.826671, y=60.184312')
        self.assertEqual(str(
            result[3]), '902 Derby Business Park: Tarvonsalmenkatu 17, x=24.835356, y=60.209017')
        self.assertEqual(str(
            result[4]), '001 Kaivopuisto: Meritori 1, x=24.9502114714031, y=60.155369615074')
        self.assertEqual(str(
            result[5]), '002 Laivasillankatu: Laivasillankatu 14, x=24.9565097715858, y=60.1609890692806')
        self.assertEqual(str(
            result[6]), '405 Jollas: Jollaksentie 33, x=25.0616678668253, y=60.1644074899774')

    def test_reads_and_parses_test_file_with_some_invalid_stations(self):
        result = self.service.parse_csv(
            './src/tests/data/invalid_stations_test.csv')

        self.assertEqual(len(result), 2)
        self.assertEqual(
            str(result[0]), '501 Hanasaari: Hanasaarenranta 1, x=24.840319, y=60.16582')
        self.assertEqual(str(
            result[1]), '001 Kaivopuisto: Meritori 1, x=24.9502114714031, y=60.155369615074')
