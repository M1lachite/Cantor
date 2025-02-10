import requests
from flask import jsonify, request
from app.extentions import db
from app.models.exchange import ExchangeRecord

class Cantor:
    """
    A class to represent a currency exchange operation.
    Attributes:
    ----------
    currency_one : str
        The currency to exchange from.
    currency_two : str
        The currency to exchange to.
    amount : float
        The amount of currency to exchange.
    date : str
        The date of the exchange rate to use.
    currency_service : CurrencyService
        An instance of a service to fetch exchange rates.
    mid_rates : dict
        A dictionary to store mid exchange rates for the currencies.
    """
    def __init__(self, currency_one, currency_two, amount, date, CurrencyService):
        """
        Constructs all the necessary attributes for the Cantor object.
        Parameters:
        ----------
        currency_one : str
            The currency to exchange from.
        currency_two : str
            The currency to exchange to.
        amount : float
            The amount of currency to exchange.
        date : str
            The date of the exchange rate to use.
        CurrencyService : CurrencyService
            An instance of a service to fetch exchange rates.
        """
        self.currency_one = currency_one
        self.currency_two = currency_two
        self.amount = amount
        self.date = date
        self.currency_service = CurrencyService
        self.mid_rates = {}
        
        
    def exchange(self):
        """
        Perform the currency exchange operation.
        """
        if self._is_same_currency():
            return self._handle_same_currency()
        
        if "pln" in (self.currency_one, self.currency_two):
            return self.exchange_with_pln()
        else:
            return self.exchange_between_foreign_currencies()

    def exchange_with_pln(self):
        """
        Perform the currency exchange operation when one of the currencies is PLN.
        """
        non_pln_currency = self.currency_two if self.currency_one == "pln" else self.currency_one
        
        rate = self.currency_service.fetch_exchange_rate(non_pln_currency, self.date)
        self.mid_rates[non_pln_currency] = rate
        
        result = self.amount / rate if self.currency_one == "pln" else self.amount * rate
        result = round(result, 2)
        
        self.save_to_db(rate, result)
        
        return f"{self.amount} {'PLN' if self.currency_one == 'pln' else non_pln_currency} = {result} {'PLN' if self.currency_one != 'pln' else non_pln_currency}"

    def exchange_between_foreign_currencies(self):
        """
        Perform the currency exchange operation between two foreign currencies.
        """
        rate_one = self.currency_service.fetch_exchange_rate(self.currency_one, self.date)
        rate_two = self.currency_service.fetch_exchange_rate(self.currency_two, self.date)
        
        self.mid_rates[self.currency_one] = rate_one
        self.mid_rates[self.currency_two] = rate_two
        
        result = (self.amount * rate_one) / rate_two
        result = round(result, 2)
        
        self.save_to_db(rate_one / rate_two, result)
        
        return f"{self.amount} {self.currency_one} = {result} {self.currency_two}, mid rates: {self.mid_rates}"

    def get_data(self):
        """
        Get the result of the currency exchange operation.
        """
        return self.exchange()
    
    def save_to_db(self, rate, result):
        """
        Save the exchange operation to the database.
        """
        rate = round(rate, 2)
        record = ExchangeRecord(
            currency_one=self.currency_one,
            currency_two=self.currency_two,
            amount=self.amount,
            date=self.date,
            exchange_rate=rate,
            result=result
        )
        db.session.add(record)
        db.session.commit()
    
    def _is_same_currency(self):
        """Check if the user is exchanging the same currency."""
        return self.currency_one == self.currency_two

    def _handle_same_currency(self):
        """Handle the case where both currencies are the same (rate = 1.0)."""
        rate = 1.0
        result = self.amount
        self.save_to_db(rate, result)
        return f"{self.amount} {self.currency_one} = {result} {self.currency_two}"
