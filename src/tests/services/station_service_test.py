import unittest
from services.station_service import StationService


class TestStationService(unittest.TestCase):
    def setUp(self):
        self.service = StationService()

    def test_parses_valid_string(self):
        result = self.service.parse_station(
            '1,501,Hanasaari,Hanaholmen,Hanasaari,Hanasaarenranta 1,\
Hanaholmsstranden 1,Espoo,Esbo,CityBike Finland,10,24.840319,60.16582'
        )

        self.assertEqual(result.station_id, '501')
        self.assertEqual(result.name_fi, 'Hanasaari')
        self.assertEqual(result.name_sv, 'Hanaholmen')
        self.assertEqual(result.name_en, 'Hanasaari')
        self.assertEqual(result.address_fi, 'Hanasaarenranta 1')
        self.assertEqual(result.address_sv, 'Hanaholmsstranden 1')
        self.assertEqual(result.city_fi, 'Espoo')
        self.assertEqual(result.city_sv, 'Esbo')
        self.assertEqual(result.operator, 'CityBike Finland')
        self.assertEqual(result.capacity, 10)
        self.assertEqual(result.x_coord, 24.840319)
        self.assertEqual(result.y_coord, 60.16582)

    def test_parses_valid_string_for_station_in_Helsinki(self):
        result = self.service.parse_station(
            '111,001,Kaivopuisto,Brunnsparken,Kaivopuisto,Meritori 1,Havstorget 1, , , ,30,24.9502114714031,60.155369615074'
        )

        self.assertEqual(result.station_id, '001')
        self.assertEqual(result.name_fi, 'Kaivopuisto')
        self.assertEqual(result.name_sv, 'Brunnsparken')
        self.assertEqual(result.name_en, 'Kaivopuisto')
        self.assertEqual(result.address_fi, 'Meritori 1')
        self.assertEqual(result.address_sv, 'Havstorget 1')
        self.assertEqual(result.city_fi, 'Helsinki')
        self.assertEqual(result.city_sv, 'Helsingfors')
        self.assertEqual(result.operator, '')
        self.assertEqual(result.capacity, 30)
        self.assertEqual(result.x_coord, 24.9502114714031)
        self.assertEqual(result.y_coord, 60.155369615074)
