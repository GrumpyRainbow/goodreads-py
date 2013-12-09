import goodreads
import datetime
import httpretty
import urllib

from nose.tools import eq_, raises

def test_client_instance_is_created():
    """Test to see if an instance of Client is created from goodreads.Client"""
    client = goodreads.Client()
    assert isinstance(client, goodreads.Client)

def test_kwargs_parsing_valid():
    """Test that valid kwargs are stored as properties on the client."""
    client = goodreads.Client(client_id='foo', client_secret='foo')
    eq_('foo', client.client_id)
    eq_('foo', client.client_secret)

def test_host_is_set():
    """Test that verifies that the host is set properly."""
    client = goodreads.Client()
    eq_("https://www.goodreads.com/", client.host)

@httpretty.activate
def test_book_title():
    """Test that verifies information about a book is done properly."""
    client = goodreads.Client(client_id="123abc")

    base_url = "https://www.goodreads.com/"
    api_call = "book/title.xml?"
    query_dict = { 'author' : 'Chuck Palahniuk', 'title' : 'Fight Club' }

    url = base_url + api_call + urllib.urlencode(query_dict)

    sample_response = open('test/fixtures/book_title_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    book = client.book_title(author='Chuck Palahniuk', book='Fight Club')

    eq_('Fight Club', book.title)
    eq_('5759', book.id)
    eq_(list, type(book.authors))
    for author in book.authors:
        eq_('2546', author.id)
        eq_('Chuck Palahniuk', author.name)

@httpretty.activate
def test_author_by_id():
    """Test that verifies information about an author is done properly."""
    client = goodreads.Client(client_id="123abc")

    base_url = "https://www.goodreads.com/"
    api_call = "author/show.xml?"
    query_dict = { 'id' : '2546' }

    url = base_url + api_call + urllib.urlencode(query_dict)

    sample_response = open('test/fixtures/author_by_id_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    author = client.author_by_id(id='2546')

    eq_('2546', author.id)
    eq_('Chuck Palahniuk', author.name)

@httpretty.activate
def test_get_author_id():
    """Test that verifies that an author's id is properly returned."""
    client = goodreads.Client(client_id="123abc")

    base_url = "https://www.goodreads.com/"
    api_call = "api/author_url/Chuck+Palahniuk?key=123abc"

    url = base_url + api_call

    sample_response = open('test/fixtures/get_author_id_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    author_id = client.get_author_id('Chuck Palahniuk')

    eq_('2546', author_id)
