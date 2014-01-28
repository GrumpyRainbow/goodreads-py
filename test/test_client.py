# Local
import goodreads
from mock_session import MockSession

# Third Party
import datetime
import httpretty
import urllib
from nose.tools import eq_, raises


BASE_URL = "https://www.goodreads.com/"


# Helper Methods

def get_client(client_id="123abc", mock_session=False):
    client = goodreads.Client(client_id=client_id)
    if mock_session:
        client.session = goodreads.GoodreadsSession("123abc", "456def",
                                                    "789ghi", "101112jkl")
        client.session.session = MockSession()
    return client

def build_url(api_call, query_dict={}):
    return BASE_URL + api_call + urllib.urlencode(query_dict)


# Testing methods

def test_client_instance_is_created():
    """Test to see if an instance of Client is created from goodreads.Client"""
    client = goodreads.Client()
    assert isinstance(client, goodreads.Client)

def test_kwargs_parsing_valid():
    """Valid kwargs are stored as properties on the client."""
    client = goodreads.Client(client_id='foo', client_secret='foo')
    eq_('foo', client.client_id)
    eq_('foo', client.client_secret)

def test_host_is_set():
    """Verifies that the host is set properly."""
    client = goodreads.Client()
    eq_("https://www.goodreads.com/", client.host)

@httpretty.activate
def test_book_title():
    """Verifies information about a book is done properly."""
    client = get_client()
    
    # Prepare URL that will be requested
    api_call = "book/title.xml?"
    query_dict = { 'author' : 'Chuck Palahniuk', 'title' : 'Fight Club' }
    url = build_url(api_call, query_dict)
    
    # Fetch sample response
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
    """Verifies information about an author is done properly."""
    client = get_client()
    
    # Prepare URL that will be requested
    api_call = "author/show.xml?"
    query_dict = { 'id' : '2546' }
    url = build_url(api_call, query_dict)
    
    # Fetch sample response
    sample_response = open('test/fixtures/author_by_id_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    author = client.author_by_id(id='2546')

    eq_('2546', author.id)
    eq_('Chuck Palahniuk', author.name)

    expected_books = ['Fight Club', 'Choke', 'Invisible Monsters',
                     'Survivor', 'Lullaby', 'Haunted', 'Diary', 'Rant',
                     'Snuff', 'Stranger Than Fiction']

    eq_(expected_books, [book.title for book in author.books])

@httpretty.activate
def test_get_author_id():
    """Verifies that an author's id is properly returned."""
    client = get_client()
    
    # Prepare URL that will be requested
    api_call = "api/author_url/Chuck+Palahniuk?key=123abc"
    url = BASE_URL + api_call
        
    # Fetch sample response
    sample_response = open('test/fixtures/get_author_id_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    author_id = client.get_author_id('Chuck Palahniuk')

    eq_('2546', author_id)

@httpretty.activate
def test_get_book_id():
    """Verifies a book's ID from ISBN"""
    client = get_client()
    
    # Prepare URL that will be requested
    api_call = "book/isbn_to_id/0393327345?key=123abc"
    url = BASE_URL + api_call
    
    # Fetch sample response
    sample_response = open('test/fixtures/get_book_id_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    book_id = client.get_book_id('0393327345')

    eq_('5759', book_id)


@httpretty.activate
def test_get_auth_user_id():
    """Verifies a retrieved authenticated user's ID (and name)"""
    client = get_client(mock_session=True)

    # Prepare URL that will be requested
    url = build_url("api/auth_user?format=xml")
    
    # Fetch sample response
    sample_response = open('test/fixtures/get_auth_user_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    user_id, user_name = client.get_auth_user()

    eq_('1374963', user_id)
    eq_('Zachariah Kendall', user_name)


@httpretty.activate
def test_get_friends():
    """Verifies getting user's friends list"""
    client = get_client(mock_session=True)

    # Prepare URL that will be requested
    user_id = "1374963"
    url = build_url("friend/user/"+user_id+"?", {'page':'1', 'format':'xml', })

    # Fetch sample response
    sample_response = open('test/fixtures/get_friends_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    friends = client.get_friends(user_id, num=30)

    eq_('12315703', friends[0][0])
    eq_('Kelli', friends[0][1])

@httpretty.activate
def test_compare_books():
    """Verifies getting book comparison between authenticated and another user"""
    client = get_client(mock_session=True)

    # Prepare URL that will be requested
    user_id = "22056220"
    url = build_url("user/compare/"+user_id+"?", {'format':'xml', })

    # Fetch sample response
    sample_response = open('test/fixtures/compare_books_response.xml')
    body = sample_response.read()

    httpretty.register_uri(httpretty.GET, url, body=body, status=200)

    comparison = client.compare_books(user_id)

    eq_('70', comparison.not_in_common)
    eq_('8.16', comparison.your_library_percent)
    eq_('31.37', comparison.their_library_percent)
    eq_('392', comparison.your_total_books_count)
    eq_('102', comparison.their_total_books_count)
    eq_('32', comparison.common_count)
    eq_('The Time Machine', comparison.reviews[10]['title'])
    eq_('4', comparison.reviews[10]['your_rating'])
    eq_('3', comparison.reviews[10]['their_rating'])






