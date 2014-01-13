import goodreads
from rauth.service import OAuth1Session
import requests

class MockSession(OAuth1Session):

    def __init__(self, client):
        self.client = client

    def post(self, url, data=None, **kwargs):
        """ """
        pass


    def get(self, url, **kwargs):
        """ """
        response = requests.get(url)
        return response

