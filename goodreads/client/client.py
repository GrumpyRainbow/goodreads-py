import datetime

from author import Author
from book import Book
from request import GoodreadsRequest, GoodreadsRequestError

class Client:
    """A client for interacting with Goodreads resources."""

    host = "https://www.goodreads.com/"

    def __init__(self, **kwargs):
        """Create a client instance using the provided options.
        The passed options should be passed as kwargs.
        """
        self.client_id     = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
        self.query_dict = { 'key' : self.client_id }

    def book_title(self, **query_dict):
        """ Get information about a book."""
        goodreads_request = GoodreadsRequest("book/title.xml", query_dict, self)
        response = goodreads_request.request()
        return Book(response['book'])

    def author_by_id(self, **query_dict):
        """ Get information about an author."""
        goodreads_request = GoodreadsRequest("author/show.xml", query_dict, self)
        response = goodreads_request.request()
        return Author(response['author'])

    def author_by_name(self, **query_dict):
        """ Get information about an author by name."""
        goodreads_request = GoodreadsRequest("api/author_url/", query_dict, self)
        response = goodreads_request.request()
        author_id = response['author']['@id']
        return self.author_by_id(id=author_id)
