from datetime import datetime
from entities.journey import Journey


class JourneyService:
    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_journey(text: str) -> Journey:
        parts = text.split(',')
        dep_time = datetime.fromisoformat(parts[0])
        ret_time = datetime.fromisoformat(parts[1])
        dep_station_id = parts[2]
        dep_station_name = parts[3]
        ret_station_id = parts[4]
        ret_station_name = parts[5]
        distance = int(parts[6])
        duration = int(parts[7])

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
