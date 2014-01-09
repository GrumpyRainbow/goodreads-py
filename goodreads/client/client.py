import datetime
import urllib
import webbrowser

from author import Author
from book import Book
from request import GoodreadsRequest, GoodreadsRequestError
from session import GoodreadsSession

class Client:
    """ A client for interacting with Goodreads resources."""

    host = "https://www.goodreads.com/"
    session = None

    def __init__(self, **kwargs):
        """
        Create a client instance using the provided options.
        The passed options should be passed as kwargs.
        """
        self.client_id     = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
        self.query_dict = { 'key' : self.client_id }

    def authenticate(self, access_token=None, access_token_secret=None):
        """ Go through OAuth process """
        self.session = GoodreadsSession(self.client_id, self.client_secret,
                                       access_token, access_token_secret)

        if access_token and access_token_secret:
            session.oath_resume()
        else: # Access not yet granted, allow via browser
            url = self.session.oath_start()
            webbrowser.open(url)
            while raw_input('Have you authorized me? (y/n) ') != 'y':
                pass
            self.session.oauth_finish()

    def book_title(self, **query_dict):
        """
        Get information about a book.
        Input Example: {'author' : 'Chuck Palahniuk', 'title' : 'Fight Club'}
        """
        goodreads_request = GoodreadsRequest("book/title.xml", query_dict, self)
        response = goodreads_request.request()
        return Book(response['book'])

    def author_by_id(self, **query_dict):
        """
        Get information about an author from their id.
        Input example: { 'id' : '2546' }
        """
        goodreads_request = GoodreadsRequest("author/show.xml", query_dict, self)
        response = goodreads_request.request()
        return Author(response['author'])

    def get_author_id(self, name):
        """ Get the id of an author given the name."""
        name = urllib.quote_plus(name)
        goodreads_request = GoodreadsRequest("api/author_url/"+name+'?', {}, self)
        response = goodreads_request.request()
        return response['author']['@id']

    def get_book_id(self, isbn):
        """ Get book id given the isbn. """
        goodreads_request = GoodreadsRequest("book/isbn_to_id/"+isbn+'?', {}, self)
        response = goodreads_request.request(return_raw=True)
        return response

    def get_friends(self):
        pass