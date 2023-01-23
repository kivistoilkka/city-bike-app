import csv
from datetime import datetime, timedelta
from entities.journey import Journey


class JourneyService:
    def __init__(self) -> None:
        pass

    def parse_csv(self, file) -> list:
        journeys = []
        with open(file, encoding='utf-8') as csv_file:
            for line in csv.reader(csv_file, quotechar='"', delimiter=','):
                if line[0] == 'Departure':
                    continue
                try:
                    journey = self.parse_journey(line)
                    journeys.append(journey)
                except ValueError:
                    continue
        return journeys

    def validate_journey(self, journey: Journey) -> bool:
        if (journey.return_time - journey.departure_time) < timedelta(0):
            return False
        if int(journey.departure_station_id) < 0:
            return False
        if int(journey.return_station_id) < 0:
            return False
        if journey.distance < 10:
            return False
        if journey.duration < 10:
            return False
        return True

    def parse_journey(self, line: list) -> Journey:
        dep_time = datetime.fromisoformat(line[0])
        ret_time = datetime.fromisoformat(line[1])
        dep_station_id = line[2]
        dep_station_name = line[3]
        ret_station_id = line[4]
        ret_station_name = line[5]
        distance = int(line[6])
        duration = int(line[7])

        journey = Journey(
            dep_time,
            ret_time,
            dep_station_id,
            dep_station_name,
            ret_station_id,
            ret_station_name,
            distance,
            duration
        )

        validation_result = self.validate_journey(journey)
        if not validation_result:
            raise ValueError
        return journey
