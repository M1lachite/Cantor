from datetime import datetime, timedelta

class BaseService:
    """
    BaseService is a class that provides functionality to calculate a specific date based on the current date
    and generate a URL for fetching exchange rates from the NBP API.
    Attributes:
        today (datetime): The current date and time.
        days_to_subtract (int): The number of days to subtract from the current date to get the calculated date.
        calculated_date (datetime): The date calculated by subtracting days_to_subtract from today.
        url_template (str): The template URL for fetching exchange rates from the NBP API.
    """ 
    def __init__(self):
        """
        Initializes the BaseService instance by setting the current date, calculating the date to be used,
        and defining the URL template for the NBP API.
        """
        self.today = datetime.now()
        weekday = self.today.weekday()
        self.days_to_subtract = 0 if weekday in range(0, 5) else 1 if weekday == 5 else 2
        self.calculated_date = self.today - timedelta(days=self.days_to_subtract)
        self.url_template = "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/"
        self.url_table = "http://api.nbp.pl/api/exchangerates/tables/A/{date}/?format=json"
        
    def get_url(self, currency, date):
        """
        Generates a URL for fetching exchange rates from the NBP API for a given currency and date.
        Args:
            currency (str): The currency code (e.g., 'USD', 'EUR').
            date (str): The date for which to fetch the exchange rate in 'YYYY-MM-DD' format.
        Returns:
            str: The formatted URL for the NBP API.
        """
        return self.url_template.format(currency=currency, date=date)
        
    @property
    def date(self):
        """
        Returns the calculated date in 'YYYY-MM-DD' format.
        Returns:
            str: The calculated date as a string.
        """
        return self.calculated_date.strftime("%Y-%m-%d")
    
    def get_table_url(self, date):
        """
        Generates a URL for fetching the exchange rate table from the NBP API for a given date.
        Args:
            date (str): The date for which to fetch the exchange rate table in 'YYYY-MM-DD' format.
        Returns:
            str: The formatted URL for the NBP API table.
        """
        return self.url_table.format(date=date)