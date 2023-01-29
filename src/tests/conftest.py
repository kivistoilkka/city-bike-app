from os import getenv
import pytest
from src.app_factory import AppFactory

@pytest.fixture
def app():
    app = AppFactory().create_app(True)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("TEST_DATABASE_URL")
    return app
