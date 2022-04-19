from xml.dom import ValidationErr
from pydantic import BaseModel, validator
from flask import render_template, request, session, redirect, url_for, flash, current_app

from project import database
from . import stock_blueprint
from ..models import Stock

################
# Helper Class #
################
class StockModel(BaseModel):
    """Class for parsing new stock data from a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()


@stock_blueprint.before_request
def stocks_before_request():
    current_app.logger.info('Calling before_request() for the stock application...')

@stock_blueprint.after_request
def stocks_after_request(response):
    current_app.logger.info('Calling after_request() for the stock application...')
    return response

@stock_blueprint.teardown_request
def stocks_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stock application...')

@stock_blueprint.route('/')
def index():
    current_app.logger.info('Calling the index() function.')
    return render_template('stocks/index.html')

@stock_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            new_stock = Stock(
                stock_data.stock_symbol,
                stock_data.number_of_shares,
                stock_data.purchase_price)
            database.session.add(new_stock)
            database.session.commit()

            flash(f"Added new stock ({ stock_data.stock_symbol })!", 'success')
            current_app.logger.info(f"Added new stock ({ request.form['stock_symbol'] })!")
            return redirect(url_for('stocks.list_stocks'))
        except ValidationErr as e:
            print(e)

    return render_template('stocks/add_stock.html')


@stock_blueprint.route('/stocks')
def list_stocks():
    stocks = Stock.query.order_by(Stock.id).all()
    return render_template('stocks/stocks.html', stocks=stocks)
