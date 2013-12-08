import httplib2
import urllib
import xmltodict
import datetime

class GoodreadsRequestError(Exception):
    def __init__(self, error_msg, url):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        return self.error_msg + "\n" + self.url

class GoodreadsRequest:
    def __init__(self, path, additional_query_info, client_instance):
        self.query_dict = dict(client_instance.query_dict.items() + additional_query_info.items())
        self.host = client_instance.host
        self.path = path
        if len(additional_query_info) > 0:
            self.path += '?'

    def request(self):
        h = httplib2.Http('.cache')
        url_extension = self.path + urllib.urlencode(self.query_dict)
        response = h.request(self.host + url_extension, "GET")
        data_dict = xmltodict.parse(response[-1])
        if data_dict.has_key('error'):
            raise GoodreadsRequestError(data_dict['error'], url_extension)
        return data_dict['GoodreadsResponse']

class GoodreadObject:
    def __init__(self, goodread_dict_dict):
        for key, val in goodread_dict_dict.items():
            self.__class__.__dict__[key] = val

class Author:
    def __init__(self, author_dict):
        for key, val in author_dict.items():
            if key == 'books':
                books = []
                for book_dict in author_dict[key]['book']:
                    print book_dict['title']
                    books.append(Book(book_dict))
                self.__class__.__dict__[key] = books
                continue
            self.__class__.__dict__[key] = val

class SimilarBook(GoodreadObject):
    def __init__(self, similar_book_dict):
        GoodreadObject.__init__(self, similar_book_dict)

class Book:
    def __init__(self, book_dict):
        for key, val in book_dict.items():
            if key == 'authors':
                authors = []
                for author_dict in book_dict[key].values():
                    authors.append(Author(author_dict))
                self.__class__.__dict__[key] = authors
                continue
            if key == 'similar_books':
                sim_books = []
                for sim_book_list in book_dict[key].values():
                    for sim_book_dict in sim_book_list:
                        sim_books.append(SimilarBook(sim_book_dict))
                self.__class__.__dict__[key] = sim_books
                continue
            self.__class__.__dict__[key] = val
        #self.__class__.__dict__['publication_date'] = self.publication_date()

    def publication_date(self):
        year = int(self.publication_year)
        month = int(self.publication_month)
        day = int(self.publication_day)
        return datetime.date(year, month, day)

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
