from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import object_session
from src.repositories.database import db
from src.models.journey import Journey


class Station(db.Model):
    id = Column(Integer, primary_key=True)
    name_fi = Column(String)
    address_fi = Column(String)
    x_coord = Column(Numeric(asdecimal=False))
    y_coord = Column(Numeric(asdecimal=False))
    departures = db.relationship('Journey', backref='journey')

    @property
    def returns(self):
        return object_session(self).query(Journey).filter(Journey.return_station == self.id).count()

    def __init__(self, id, name_fi, address_fi, x_coord, y_coord):
        self.id = id
        self.name_fi = name_fi
        self.address_fi = address_fi
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self) -> str:
        return f'{str(self.id).zfill(3)} {self.name_fi}: {self.address_fi}, \
x={self.x_coord}, y={self.y_coord}'

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'name_fi': self.name_fi,
            'address_fi': self.address_fi,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'departures': len(self.departures),
            'returns': self.returns
        }
