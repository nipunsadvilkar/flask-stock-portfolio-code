import logging
from logging.handlers import RotatingFileHandler

from flask.logging import default_handler
from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)

app.secret_key = 'W\x13)i^eK啓HT2\x12tBac0\x1d(\t50u'

# Logging Configuration
file_handler = RotatingFileHandler('flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.removeHandler(default_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')

from project.users import users_blueprint
from project.stocks import stock_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(stock_blueprint)

