import unittest
import pytest
from src.repositories.journey_repository import JourneyRepository
from src.repositories.database import db


class TestJourneyRepository(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, app):
        self.app = app

    def setUp(self):
        self.repository = JourneyRepository(db)

    def test_get_defined_range_list_of_all_journeys_as_Journey_objects_in_id_number_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_journeys_by_id(0, 10)

        self.assertEqual(len(result), 10)
        self.assertEqual(
            str(result[0]),
            '2021-05-31 23:57:25 094 -> 100 2021-06-01 00:05:46, 2043 m, 500 sec'
        )
        self.assertEqual(result[0].id, 1)
        self.assertEqual(
            str(result[9]),
            '2021-05-31 23:50:19 116 -> 145 2021-06-01 00:05:58, 3248 m, 935 sec'
        )
        self.assertEqual(result[9].id, 10)

    def test_get_defined_range_list_of_all_journeys_as_Journey_objects_in_decreasing_time_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_journeys_by_time(
                6, 11, True)

        self.assertEqual(len(result), 5)
        self.assertEqual(
            str(result[0]),
            '2021-05-31 23:54:11 034 -> 081 2021-06-01 00:17:11, 2550 m, 1377 sec'
        )
        self.assertEqual(result[0].id, 7)
        self.assertEqual(
            str(result[4]),
            '2021-05-31 23:50:05 147 -> 232 2021-06-01 00:01:22, 1633 m, 672 sec'
        )
        self.assertEqual(result[4].id, 11)

    def test_get_defined_range_list_of_all_journeys_as_Journey_objects_in_increasing_time_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_journeys_by_time(
                0, 3, False)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            str(result[0]),
            '2021-05-31 23:28:16 082 -> 084 2021-05-31 23:31:00, 665 m, 159 sec'
        )
        self.assertEqual(result[0].id, 33)
        self.assertEqual(
            str(result[2]),
            '2021-05-31 23:30:06 547 -> 547 2021-05-31 23:49:17, 739 m, 1146 sec'
        )
        self.assertEqual(result[2].id, 31)

    def test_get_defined_range_list_of_all_journeys_as_Journey_objects_in_decreasing_distance_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_journeys_by_distance(
                0, 2)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            str(result[0]),
            '2021-05-31 23:31:27 315 -> 272 2021-05-31 23:57:24, 5495 m, 1553 sec'
        )
        self.assertEqual(
            str(result[1]),
            '2021-05-31 23:53:04 240 -> 281 2021-06-01 00:14:52, 5366 m, 1304 sec'
        )

    def test_get_defined_range_list_of_all_journeys_as_Journey_objects_in_decreasing_duration_order(self):
        with self.app.app_context():
            result = self.repository.get_range_from_all_journeys_by_duration(
                0, 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            str(result[0]),
            '2021-05-31 23:30:45 573 -> 511 2021-06-01 15:45:49, 2834 m, 58499 sec'
        )
