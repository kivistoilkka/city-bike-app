import csv
from datetime import datetime, timedelta
from src.models.journey import Journey


class JourneyService:
    def __init__(self, journey_repository, station_repository):
        self.journey_repository = journey_repository
        self.station_repository = station_repository

    def parse_csv(self, file, logs=False) -> list:
        journeys = []
        with open(file, encoding='utf-8') as csv_file:
            for line in csv.reader(csv_file, quotechar='"', delimiter=','):
                if line[0] == 'Departure':
                    continue
                try:
                    journey = self.parse_journey(line)
                    journeys.append(journey)
                    if logs:
                        print(journey)
                except ValueError:
                    continue
        return journeys

    def validate_journey(self, journey: Journey) -> bool:
        if (journey.return_time - journey.departure_time) < timedelta(0):
            return False
        if journey.distance < 10:
            return False
        if journey.duration < 10:
            return False
        return True

    def parse_journey(self, line: list) -> Journey:
        dep_time = datetime.fromisoformat(line[0])
        ret_time = datetime.fromisoformat(line[1])
        dep_station_id = int(line[2])
        if dep_station_id < 0:
            raise ValueError
        dep_station = self.station_repository.get_station(dep_station_id)
        ret_station_id = int(line[4])
        if ret_station_id < 0:
            raise ValueError
        ret_station = self.station_repository.get_station(ret_station_id)
        distance = int(line[6])
        duration = int(line[7])

        journey = Journey(
            dep_time,
            ret_time,
            dep_station.id,
            ret_station.id,
            distance,
            duration
        )

        validation_result = self.validate_journey(journey)
        if not validation_result:
            raise ValueError
        return journey
