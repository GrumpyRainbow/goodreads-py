from urllib import urlencode

class Client:
    """A client for interacting with Goodreads resources."""

    def __init__(self, **kwargs):
        """Create a client instance using the provided options.
        The passed options should be passed as kwargs.
        """
        self.client_id     = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
