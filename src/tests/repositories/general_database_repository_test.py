import unittest
import pytest
from src.repositories.general_database_repository import GeneralDatabaseRepository


class TestStationRepository(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, app):
        self.app = app

    def setUp(self) -> None:
        self.repository = GeneralDatabaseRepository()

    def test_get_database_info_works(self):
        with self.app.app_context():
            result = self.repository.get_database_info()
            self.assertEqual(
                result,
                {
                    "station_count": 72,
                    "journey_count": 48
                }
            )
