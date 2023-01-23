class Journey:
    def __init__(self,
                 dep_time,
                 ret_time,
                 dep_station_id,
                 dep_station_name,
                 ret_station_id,
                 ret_station_name,
                 distance,
                 duration
                 ) -> None:
        self.departure_time = dep_time
        self.return_time = ret_time
        self.departure_station_id = dep_station_id
        self.departure_station_name = dep_station_name
        self.return_station_id = ret_station_id
        self.return_station_name = ret_station_name
        self.distance = distance
        self.duration = duration

    def __str__(self) -> str:
        return f'{self.departure_station_id} {self.departure_station_name} -> \
{self.return_station_id} {self.return_station_name}, \
{self.distance} m, {self.duration} sec'
