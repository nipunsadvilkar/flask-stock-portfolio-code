import flask
import pytest
from flask import current_app

from project import create_app
from project.models import Stock


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    with flask_app.test_client() as testing_client:

        with flask_app.app_context():
            current_app.logger.info("Inside a testing fixture...")

        yield testing_client

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('TSLA', '23', '224.97')
    return stock