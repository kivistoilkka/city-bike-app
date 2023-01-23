from datetime import datetime
from entities.journey import Journey


class JourneyService:
    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_journey(line: list) -> Journey:
        dep_time = datetime.fromisoformat(line[0])
        ret_time = datetime.fromisoformat(line[1])
        dep_station_id = line[2]
        dep_station_name = line[3]
        ret_station_id = line[4]
        ret_station_name = line[5]
        distance = int(line[6])
        duration = int(line[7])

        return Journey(
            dep_time,
            ret_time,
            dep_station_id,
            dep_station_name,
            ret_station_id,
            ret_station_name,
            distance,
            duration
        )
