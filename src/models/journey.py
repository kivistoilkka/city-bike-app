from datetime import datetime
import sqlalchemy as sa
from src.models.station import Station
from src.repositories.database import db


class Journey(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    departure_time = sa.Column(sa.DateTime)
    return_time = sa.Column(sa.DateTime)
    departure_station = sa.Column(sa.ForeignKey(Station.id))
    return_station = sa.Column(sa.ForeignKey(Station.id))
    distance = sa.Column(sa.Integer)
    duration = sa.Column(sa.Integer)

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
        return f'{str(self.departure_station.id).zfill(3)} \
{self.departure_station.name_fi} -> \
{str(self.return_station.id).zfill(3)} {self.return_station.name_fi}, \
{self.distance} m, {self.duration} sec'
