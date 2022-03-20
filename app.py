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

@app.route('/')
def index():
    app.logger.info('Calling the index() function.')
    return render_template('index.html')

@app.route('/about')
def about():
    flash('Thanks for learning about this site', 'info')
    return render_template('about.html', company_name='Testdriven.io')

@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        session['stock_symbol'] = request.form['stock_symbol']
        session['number_of_shares'] = request.form['number_of_shares']
        session['purchase_price'] = request.form['purchase_price']
        flash(f"Added new stock ({ request.form['stock_symbol'] })!", 'success')

        app.logger.info(f"Added new stock ({ request.form['stock_symbol'] })!")

        return redirect(url_for('list_stocks'))

    return render_template('add_stock.html')

@app.route('/stocks')
def list_stocks():
    return render_template('stocks.html')