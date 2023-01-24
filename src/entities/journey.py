from datetime import datetime
from entities.station import Station


class Journey:
    def __init__(self,
                 dep_time: datetime,
                 ret_time: datetime,
                 dep_station: Station,
                 ret_station: Station,
                 distance: int,
                 duration: int
                 ) -> None:
        self.departure_time = dep_time
        self.return_time = ret_time
        self.departure_station = dep_station
        self.return_station = ret_station
        self.distance = distance
        self.duration = duration

    def __str__(self) -> str:
        return f'{str(self.departure_station.station_id).zfill(3)} \
{self.departure_station.name_fi} -> \
{str(self.return_station.station_id).zfill(3)} {self.return_station.name_fi}, \
{self.distance} m, {self.duration} sec'
