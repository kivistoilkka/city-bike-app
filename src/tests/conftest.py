from os import getenv
import pytest
from src.app_factory import AppFactory


@pytest.fixture
def app():
    app = AppFactory().create_app(testing=True)
    return app
