from urllib import response


def test_registration_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/register')
    assert response.status_code  == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Registration' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data

def test_valid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with valid data
    THEN check the response is valid and the user is registered
    """
    response = test_client.post('/users/register',
                                data={
                                    'email': 'nipunsadvilkar@gmail.com',
                                    'password': 'LearningFromTestdriven.io'
                                    },
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Thanks for registering, nipunsadvilkar@gmail.com' in response.data

def test_invalid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with invalid data (missing password)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/register',
                                data={
                                    'email': 'nipunsadvilkar2@gmail.com',
                                    'password': ''
                                    },
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Thanks for registering, nipunsadvilkar2@gmail.com!' not in response.data
    assert b'[This field is required.]' in response.data

def test_duplicate_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register/' page is posted to (POST) with the email address for an existing user
    THEN check an error message is returned to the user
    """
    test_client.post('/users/register',
                                data={
                                    'email': 'nipunsadvilkar@gmail.com',
                                    'password': 'LearningFromTestdriven.io'
                                    },
                                follow_redirects=True)
    response = test_client.post('/users/register',
                                data={
                                    'email': 'nipunsadvilkar@gmail.com',
                                    'password': 'LearningFlaskFromTestdriven.io'
                                    },
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Thanks for registering, nipunsadvilkar@gmail.com!' not in response.data
    assert b'ERROR! Email (nipunsadvilkar@gmail.com) already exists.' in response.data


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data

def test_valid_login_and_logout(test_client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is posted to (POST) with valid credentials
    THEN check the response is valid
    """
    response = test_client.post('/users/login',
                                data={'email': 'nipunsadvilkar@gmail.com',
                                      'password': 'LearningFromTestdriven.io'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for logging in, nipunsadvilkar@gmail.com' in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Please log in to access this page.' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is posted to (POST) with valid credentials
    THEN check the response is valid
    """
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Goodbye' in  response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Please log in to access this page.' not in response.data

def test_invalid_login(test_client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is posted to (POST) with invalid credentials
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/login',
                                data={'email': 'nipunsadvilkar@gmail.com',
                                      'password': 'LearningFromTestdriven'},  # Incorrect password
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'ERROR! Incorrect login credentials.' in response.data
    assert b'Flask Stock Portfolio App' in response.data

def test_valid_login_when_logged_in_already(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
    WHEN the '/users/login' page is posted to (POST) with valid credentials for the default user
    THEN check a warning is returned to user (already logged in)
    """
    response = test_client.post('/users/login',
                                data={'email': 'nipunsadvilkar@gmail.com',
                                      'password': 'LearningFromTestdriven'},  # Incorrect password
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Already logged in!' in response.data
    assert b'Flask Stock Portfolio App' in response.data

def test_invalid_logout(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/logout' page is posted to (POST)
    THEN check that a 405 error is returned
    """
    response = test_client.post('/users/logout', follow_redirects=True)
    assert response.status_code == 405
    assert b'Goodbye' not in  response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Method Not Allowed' in response.data

def test_invalid_logout_and_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/logout' page is requested (GET) when the user is not logged in
    THEN check that the user is redirected to the login page
    """
    test_client.get('/users/logout', follow_redirects=True)  # Double-check there are no logged in users!
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Goodbye' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Login' in response.data
    assert b'Please log in to access this page' in response.data

