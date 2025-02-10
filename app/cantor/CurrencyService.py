import requests
from flask import jsonify, request

class CurrencyService:
    """
    A service class to fetch exchange rates for a given currency and date.
    Attributes:
        BaseService (object): An instance of a base service class that provides URL generation.
    """
    def __init__(self, BaseService):
        """
        Initializes the CurrencyService with a base service instance.
        Args:
            BaseService (object): An instance of a base service class.
        """
        self.BaseService = BaseService
    
    def fetch_exchange_rate(self, currency, date):
        """
        Fetches the exchange rate for a given currency on a specific date.
        Args:
            currency (str): The currency code (e.g., 'USD', 'EUR').
            date (str): The date for which to fetch the exchange rate (format: 'YYYY-MM-DD').
        Returns:
            float: The mid exchange rate for the specified currency and date.
        Raises:
            ValueError: If the request fails or the data format is invalid.
        """
        url = self.BaseService.get_url(currency, date)
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError("Failed to fetch exchange rate")
        
        data = response.json()
        rates = data.get("rates", [])
        if not rates or not isinstance(rates, list):
            raise ValueError(f"Invalid data format for {currency} on {date}")
                
        mid = rates[0].get("mid")
        if not mid:
            raise ValueError(f"Mid rate not found for {currency} on {date}")
    
        return  mid