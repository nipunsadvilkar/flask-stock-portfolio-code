import os
import logging
from logging.handlers import RotatingFileHandler

from flask.logging import default_handler
from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)

# configure the application
config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(config_type)

# Logging Configuration
file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.removeHandler(default_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')

# Import the blueprints
from project.stocks import stock_blueprint
from project.users import users_blueprint

# Register the blueprints
app.register_blueprint(stock_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')

