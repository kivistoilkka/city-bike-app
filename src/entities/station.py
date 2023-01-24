class Station:
    def __init__(self,
                 station_id: int,
                 name_fi: str,
                 #  name_sv: str,
                 #  name_en: str,
                 address_fi: str,
                 #  address_sv: str,
                 #  city_fi: str,
                 #  city_sv: str,
                 #  operator: str,
                 #  capacity: int,
                 x_coord: float,
                 y_coord: float
                 ) -> None:
        self.station_id = station_id
        self.name_fi = name_fi
        # self.name_sv = name_sv
        # self.name_en = name_en
        self.address_fi = address_fi
        # self.address_sv = address_sv
        # self.city_fi = city_fi
        # self.city_sv = city_sv
        # self.operator = operator
        # self.capacity = capacity
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self) -> str:
        return f'{str(self.station_id).zfill(3)} {self.name_fi}: {self.address_fi}, \
x={self.x_coord}, y={self.y_coord}'
