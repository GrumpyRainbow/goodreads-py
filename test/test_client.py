import goodreads

from nose.tools import eq_

def test_kwargs_parsing_valid():
    """Test that valid kwargs are stored as properties on the client."""
    client = goodreads.Client(client_id='foo', client_secret='foo')
    assert isinstance(client, goodreads.Client)
    eq_('foo', client.client_id)
    eq_('foo', client.client_secret)
