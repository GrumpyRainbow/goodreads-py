import httplib2
import urllib
import xmltodict

class GoodreadsRequestError(Exception):
    """ Custom request exception """
    def __init__(self, error_msg, url):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        return self.error_msg + "\n" + self.url

class GoodreadsRequest:
    """ Handles the goodreads requests and response parsing """

    def __init__(self, path, additional_query_info, client_instance):
        """ """
        self.query_dict = dict(client_instance.query_dict.items() + additional_query_info.items())
        self.host = client_instance.host
        self.path = path
        # Will there be parameters?
        if len(self.query_dict) > 0:
            self.path += '?'

    def request(self, return_raw=False):
        """ """
        h = httplib2.Http('.cache')
        url_extension = self.path + urllib.urlencode(self.query_dict)
        response, content  = h.request(self.host + url_extension, "GET")

        # Check success
        if response['status'] != '200':
            raise GoodreadsRequestError(response['status'], url_extension)
            return

        # Some responses aren't xml structured (see get_book_id)
        if return_raw:
            return content
            
        # Parse response into dictionary
        data_dict = xmltodict.parse(content)
        if data_dict.has_key('error'):
            raise GoodreadsRequestError(data_dict['error'], url_extension)
        return data_dict['GoodreadsResponse']

