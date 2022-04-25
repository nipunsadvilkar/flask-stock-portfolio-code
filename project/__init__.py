from curses.ascii import US
from importlib.metadata import metadata
import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask.logging import default_handler

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager

#################
# Configuration #
#################

# Create a naming convention for the database tables
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# Create the instances of the Flask extensions in the global scope,
# but without any arguments passed in. These instances are not
# attached to the Flask application at this point.
database = SQLAlchemy(metadata=metadata)
db_migration = Migrate()
login = LoginManager()
login.login_view = "users.login"

########################
### Helper Functions ###
########################

def initialise_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    database.init_app(app)
    db_migration.init_app(app, database, render_as_batch=True)

    # Flask Login configuration
    login.init_app(app)
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app):
    # Import the blueprints
    from project.stocks import stock_blueprint
    from project.users import users_blueprint

    # Register the blueprints
    app.register_blueprint(stock_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')

def register_app_callbacks(app):
    @app.before_request
    def app_before_request():
        app.logger.info('Calling before_request() for the Flask application...')

    @app.after_request
    def app_after_request(response):
        app.logger.info('Calling after_request() for the Flask application...')
        return response

    @app.teardown_request
    def app_teardown_request(error=None):
        app.logger.info('Calling teardown_request() for the Flask application...')

    @app.teardown_appcontext
    def app_teardown_appcontext(error=None):
        app.logger.info('Calling app_teardown_appcontext() for the Flask application...')

def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

def configure_logging(app):
    # Logging Configuration
    file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # remove default logger configured by Flask
    app.logger.removeHandler(default_handler)

    # Log that the Flask application is starting
    app.logger.info('Starting the Flask Stock Portfolio App...')

################################
# Application Factory Function #
################################

def create_app():
    # Configure the Flask application
    app = Flask(__name__)

    # configure the application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialise_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_app_callbacks(app)
    register_error_pages(app)
    return app
