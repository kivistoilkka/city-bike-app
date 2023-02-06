import unittest
import pytest

from src.models.station import Station
from src.models.journey import Journey
from src.repositories.database import db
from src.repositories.station_repository import StationRepository
from src.repositories.journey_repository import JourneyRepository
from src.services.station_service import StationService
from src.services.journey_service import JourneyService

from src.database_builder import DatabaseBuilder


class TestDatabaseBuilder(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, app):
        self.app = app
        self.builder = DatabaseBuilder()
        self.station_repository = StationRepository(db)
        self.station_service = StationService(db, self.station_repository)
        self.journey_repository = JourneyRepository(db)
        self.journey_service = JourneyService(
            self.journey_repository, self.station_repository
        )

    def test_built_database_is_correct_size(self):
        with self.app.app_context():
            db.drop_all()
            self.builder.build_database(
                stations_created=False, station_service=self.station_service,
                journeys_created=False, journey_service=self.journey_service,
                testing=True
            )
            station_count = Station.query.count()
            journey_count = Journey.query.count()

        self.assertEqual(station_count, 72)
        self.assertEqual(journey_count, 48)
