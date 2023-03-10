import unittest
import pytest
from src.repositories.station_repository import StationRepository
from src.repositories.database import db


class TestStationRepository(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, app):
        self.app = app

    def setUp(self):
        self.repository = StationRepository(db)

    def test_finds_existing_stations_from_test_database(self):
        with self.app.app_context():
            result = self.repository.get_station(1)

        self.assertEqual(result.id, 1)
        self.assertEqual(result.name_fi, 'Kaivopuisto')
        self.assertEqual(result.address_fi, 'Meritori 1')
        self.assertEqual(result.x_coord, 24.9502114714031)
        self.assertEqual(result.y_coord, 60.155369615074)

    def test_gets_complete_list_of_all_stations_as_Station_objects_in_number_order(self):
        with self.app.app_context():
            result = self.repository.get_all_stations()

        self.assertEqual(len(result), 72)
        self.assertEqual(
            str(result[0]),
            '001 Kaivopuisto: Meritori 1, x=24.9502114714031, y=60.155369615074'
        )
        self.assertEqual(
            str(result[71]),
            '727 Ratsutori: Leppävaarankatu 1, x=24.812419, y=60.217311'
        )

    def test_gets_defined_range_list_of_all_stations_as_Station_objects_in_id_number_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_stations(3, 13)

        self.assertEqual(len(result), 10)
        self.assertEqual(
            str(result[0]),
            '009 Erottajan aukio: Eteläesplanadi 22, x=24.9441887601673, y=60.1668948711694'
        )
        self.assertEqual(
            str(result[9]),
            '041 Ympyrätalo: Porthaninrinne 1, x=24.949399999845, y=60.1808629918822'
        )

    def test_gets_correct_number_of_journeys_to_and_from_station(self):
        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(1)
        self.assertEqual(result['departures'], 1)
        self.assertEqual(result['returns'], 0)

        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(30)
        self.assertEqual(result['departures'], 3)
        self.assertEqual(result['returns'], 0)

        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(34)
        self.assertEqual(result['departures'], 1)
        self.assertEqual(result['returns'], 1)

        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(62)
        self.assertEqual(result['departures'], 0)
        self.assertEqual(result['returns'], 2)

        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(547)
        self.assertEqual(result['departures'], 3)
        self.assertEqual(result['returns'], 3)

        with self.app.app_context():
            result = self.repository.get_journeys_to_and_from_station(727)
        self.assertEqual(result['departures'], 2)
        self.assertEqual(result['returns'], 0)

    def test_returns_valueerror_if_station_missing_when_getting_journeys_from_and_to(self):
        with self.assertRaises(ValueError) as cm:
            with self.app.app_context():
                result = self.repository.get_journeys_to_and_from_station(2)
        self.assertEqual(str(cm.exception), 'Station id not in database')
