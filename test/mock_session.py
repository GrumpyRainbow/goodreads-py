import goodreads
from rauth.service import OAuth1Session
import requests

class MockSession(OAuth1Session):
    """ A mock session to bypass OAuth for testing. Make basic calls
    to retrieve fixtures from httpretty. """
    
    def __init__(self):
        pass

    def post(self, url, params={}):
        """ NOTE: This hasn't been tested yet """
        response = requests.poast(url, params=params)
        return response

    def get(self, url, params={}):
        """ """
        response = requests.get(url, params=params)
        return response

