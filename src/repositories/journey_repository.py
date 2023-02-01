from src.models.journey import Journey


class JourneyRepository:
    def __init__(self, db):
        self.db = db
