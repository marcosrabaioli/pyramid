from configparser import ConfigParser
import requests
import os
from random import randint

path = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser()
config.read(path+'/wrapper.ini')
url = config.get('quotes_api','url')


class QuotesWrapper(object):

    def get_quotes(self):

        url_quotes = url + 'quotes'
        response = requests.get(url_quotes)
        data = response.json()
        status = response.status_code
        return status, data

    def get_quote(self, number):

        url_quotes = url + 'quotes/' + number
        response = requests.get(url_quotes)
        data = response.json()
        status = response.status_code
        return status, data

    def get_quote_random(self):

        status, data = self.get_quotes()

        if status == 200:
            count_quotes = len(data['quotes'])
            random_number = randint(1, count_quotes)
            return status, {'pk': random_number, 'quote': data['quotes'][random_number]}
        else:
            return status, data


