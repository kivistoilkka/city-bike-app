import csv
from datetime import datetime, timedelta
from src.models.journey import Journey


class JourneyService:
    def __init__(self, journey_repository, station_repository):
        self.journey_repository = journey_repository
        self.station_repository = station_repository

    def validate_journey(self, journey: Journey) -> bool:
        if (journey.return_time - journey.departure_time) < timedelta(0):
            return False
        if journey.distance < 10:
            return False
        if journey.duration < 10:
            return False
        return True

    def parse_journey(self, line: list, stations: dict) -> Journey:
        dep_time = datetime.fromisoformat(line[0])
        ret_time = datetime.fromisoformat(line[1])
        dep_station_id = int(line[2])
        ret_station_id = int(line[4])
        if dep_station_id < 0 or ret_station_id < 0:
            raise ValueError
        if dep_station_id not in stations.keys() or ret_station_id not in stations.keys():
            raise ValueError
        distance = int(line[6])
        duration = int(line[7])

        journey = Journey(
            dep_time,
            ret_time,
            dep_station_id,
            ret_station_id,
            distance,
            duration
        )

        validation_result = self.validate_journey(journey)
        if not validation_result:
            raise ValueError
        return journey

    def parse_csv(self, file:str, stations:dict, logs=False) -> dict:
        journeys = {}
        with open(file, encoding='utf-8') as csv_file:
            for line in csv.reader(csv_file, quotechar='"', delimiter=','):
                if logs:
                    print('Line: ', line)
                if line[0] == 'Departure':
                    continue
                try:
                    journey = self.parse_journey(line, stations)
                    # if logs:
                    #     print('Parsed:', journey)
                        # if logs:
                        #     print('Added:', journey)
                    if str(journey) not in journeys:
                        journeys[str(journey)] = journey
                except ValueError:
                    # if logs:
                    #     print('Line rejected')
                    continue
        return journeys

    def get_journeys_in_decreasing_time_order(self, lower:int, upper:int) -> list:
        journeys = self.journey_repository.get_range_from_all_journeys_by_time(
            lower, upper, True
        )
        return list(map(lambda j: j.as_dict(), journeys))

    def get_journeys_in_increasing_time_order(self, lower:int, upper:int) -> list:
        journeys = self.journey_repository.get_range_from_all_journeys_by_time(
            lower, upper, False
        )
        return list(map(lambda j: j.as_dict(), journeys))

    def get_journeys_in_distance_order(self, lower:int, upper:int) -> list:
        journeys = self.journey_repository.get_range_from_all_journeys_by_distance(
            lower, upper
        )
        return list(map(lambda j: j.as_dict(), journeys))

    def get_journeys_in_duration_order(self, lower:int, upper:int) -> list:
        journeys = self.journey_repository.get_range_from_all_journeys_by_duration(
            lower, upper
        )
        return list(map(lambda j: j.as_dict(), journeys))
