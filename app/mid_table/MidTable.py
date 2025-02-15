from flask import Flask, request
import requests


class MidTable:
    def __init__(self, BaseService, date):
        self.date = date
        self.url = BaseService.get_table_url(date)
        
    def get_table(self):
        url = self.url
        response = requests.get(url)

        if response.status_code != 200:
            return "Table is not available."
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0 and 'rates' in data[0]:
            rates = data[0]['rates']
            return [(rate['currency'], rate['code'], rate['mid']) for rate in rates]  # Dodajemy nazwę waluty
        else:
            return "Invalid data format."
