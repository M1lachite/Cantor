from flask import render_template, request
from app.cantor import bp
from app.cantor.Cantor import Cantor
from app.cantor.CurrencyService import CurrencyService
from app.cantor.BaseService import BaseService

Service = BaseService()
date = Service.date

@bp.route('/')
def index():
    """Render the main page of the cantor application.

    Returns:
        Rendered HTML template for the index page.
    """
    return render_template('cantor/index.html')

@bp.route('/categories')
def categories():
    """Render the categories page.

    Returns:
        Rendered HTML template for the categories page.
    """
    return render_template('cantor/categories.html')

@bp.route('cantor', methods=['GET', 'POST'])
def cantor():
    """Handle currency exchange requests.

    GET: Display the currency exchange form.
    POST: Process the currency exchange based on user input.

    Form Data:
        currency_one (str): The base currency.
        currency_two (str): The target currency.
        amount (float): The amount to exchange.

    Returns:
        dict: The exchange result from the Cantor service.
    """
    currency_one = request.form.get("currency_one")
    currency_two = request.form.get("currency_two")    

    currency_service = CurrencyService(Service)
    amount = float(request.form.get("amount"))
    cantor = Cantor(currency_one, currency_two, amount, date, currency_service)
    result = cantor.get_data()
    return result
    