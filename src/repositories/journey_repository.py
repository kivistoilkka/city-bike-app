from src.models.journey import Journey


class JourneyRepository:
    def __init__(self, db):
        self.db = db

    def get_range_from_all_journeys_by_id(self, lower: int, upper: int) -> list:
        """Returns sublist of journeys from all journeys ordered by id, including
        journey in position 'lower' of the list (counting starts from 0) and excluding
        journey in position 'upper'.

        Args:
            lower (int): First position to be included, counting starts from 0
            upper (int): Position after the last to be included

        Returns:
            list: List of Journey objects in numerical order by id
        """
        journeys = Journey.query.order_by(Journey.id).limit(
            upper-lower).offset(lower).all()
        return journeys

    def get_range_from_all_journeys_by_time(self, lower: int, upper: int, decreasing:bool) -> list:
        """Returns sublist of journeys from all journeys ordered by id, including
        journey in position 'lower' of the list (counting starts from 0) and excluding
        journey in position 'upper'.

        Args:
            lower (int): First position to be included, counting starts from 0
            upper (int): Position after the last to be included
            decreading (bool): True if both original and sublist should be in decreasing
                order

        Returns:
            list: List of Journey objects in numerical order by id
        """
        if decreasing:
            journeys = Journey.query.order_by(Journey.departure_time.desc()).limit(
                upper-lower).offset(lower).all()
        else:
            journeys = Journey.query.order_by(Journey.departure_time).limit(
                upper-lower).offset(lower).all()
        return journeys
