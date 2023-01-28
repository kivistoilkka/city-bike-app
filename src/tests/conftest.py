from os import getenv
import pytest
from src import create_app

@pytest.fixture
def app():
    app = create_app(True)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("TEST_DATABASE_URL")
    return app
