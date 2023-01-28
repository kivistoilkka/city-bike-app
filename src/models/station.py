import sqlalchemy as sa
from src.repositories.database import db


class Station(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name_fi = sa.Column(sa.String)
    address_fi = sa.Column(sa.String)
    x_coord = sa.Column(sa.Numeric(asdecimal=False))
    y_coord = sa.Column(sa.Numeric(asdecimal=False))

    def __init__(self, id, name_fi, address_fi, x_coord, y_coord):
        self.id = id
        self.name_fi = name_fi
        self.address_fi = address_fi
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self) -> str:
        return f'{str(self.id).zfill(3)} {self.name_fi}: {self.address_fi}, \
x={self.x_coord}, y={self.y_coord}'
