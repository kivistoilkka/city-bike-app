from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from src.repositories.database import db


class Journey(db.Model):
    id = Column(Integer, primary_key=True)
    departure_time = Column(DateTime)
    return_time = Column(DateTime)
    departure_station = Column(Integer, ForeignKey('station.id'))
    return_station = Column(Integer)
    distance = Column(Integer)
    duration = Column(Integer)

    def __init__(self,
                 dep_time: datetime,
                 ret_time: datetime,
                 dep_station: int,
                 ret_station: int,
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
        return f'{self.departure_time} {str(self.departure_station).zfill(3)} -> \
{str(self.return_station).zfill(3)} {self.return_time}, \
{self.distance} m, {self.duration} sec'

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'departure_time': self.departure_time,
            'return_time': self.return_time,
            'departure_station': self.departure_station,
            'return_station': self.return_station,
            'distance': self.distance,
            'duration': self.duration,
        }
