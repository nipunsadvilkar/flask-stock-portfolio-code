import flask
import pytest
from flask import current_app

from project import database
from project import create_app
from project.models import Stock, User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    with flask_app.test_client() as testing_client:

        with flask_app.app_context():
            current_app.logger.info("Creating database tables in test_client fixture...")
        
            database.create_all()

        yield testing_client

        with flask_app.app_context():
            database.drop_all()

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('TSLA', '23', '224.97')
    return stock

@pytest.fixture(scope='module')
def new_user():
    user = User('nipunsadvilkar@gmail.com', 'TestDriven10')
    return user


@pytest.fixture(scope='module')
def register_default_user(test_client):
    # Register the default user
    test_client.post('/users/register',
                     data={
                         'email': 'nipunsadvilkar@gmail.com',
                         'password': 'LearningFromTestdriven.io'
                     }, follow_redirects=True)
    return

@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    test_client.post('/users/login',
                     data={
                          'email': 'nipunsadvilkar@gmail.com',
                          'password': 'LearningFromTestdriven.io'
                     },
                     follow_redirects=True
                    )
    yield

    test_client.get('/users/logout', follow_redirects=True)