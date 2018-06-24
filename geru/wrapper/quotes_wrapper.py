from configparser import ConfigParser
import requests
import os
from random import randint

path = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser()
config.read(path+'/wrapper.ini')
url = config.get('quotes_api','url')


class QuotesWrapper(object):

    @staticmethod
    def get_quotes():

        url_quotes = url + 'quotes'
        response = requests.get(url_quotes)
        data = response.json()
        status = response.status_code
        return status, data

    @staticmethod
    def get_quote(number):

        url_quotes = url + 'quotes/' + number
        response = requests.get(url_quotes)
        data = response.json()
        status = response.status_code
        return status, data

    @staticmethod
    def get_quote_random():

        status, data = QuotesWrapper.get_quotes()

        if status == 200:
            count_quotes = len(data['quotes'])
            random_number = randint(0, count_quotes)
            return status, {'pk': random_number, 'quote': data['quotes'][random_number]}
        else:
            return status, data


