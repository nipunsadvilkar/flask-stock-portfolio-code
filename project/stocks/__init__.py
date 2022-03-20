from flask import Blueprint

stock_blueprint = Blueprint('stocks', __name__, template_folder='templates')

from . import routes