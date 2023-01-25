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
