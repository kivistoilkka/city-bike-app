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
