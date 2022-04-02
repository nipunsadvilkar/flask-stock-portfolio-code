"""
This file (test_app.py) contains unit tests for the app.py file
"""
from app import app

def test_index_page(test_client):
    """
    GIVEN a Flask Application
    WHEN the `/` is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the' in response.data
    assert b'Flask Stock Portfolio App!' in response.data

def test_about(test_client):
    """
    GIVEN a Flask Application
    WHEN the `/` is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/about')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'About' in response.data
    assert b'This application is built using Flask web framework' in response.data
    assert b'Course is developed by Testdriven.io.' in response.data
