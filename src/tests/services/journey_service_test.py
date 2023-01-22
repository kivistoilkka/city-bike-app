import unittest
from datetime import datetime
from services.journey_service import JourneyService


class TestJourneyService(unittest.TestCase):
    def setUp(self):
        self.service = JourneyService()

    def test_parses_valid_string(self):
        result = self.service.parse_journey(
            '2021-05-01T00:00:11,2021-05-01T00:04:34,138,Arabiankatu,138,Arabiankatu,1057,259'
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
