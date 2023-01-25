from flask_sqlalchemy import SQLAlchemy


class Database:
    def __init__(self) -> None:
        self.db = SQLAlchemy()

db = Database().db