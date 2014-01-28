from rauth.service import OAuth1Service, OAuth1Session
import xmltodict

class GoodreadsSessionError(Exception):
    """ Custom request exception """
    def __init__(self, error_msg):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        return self.error_msg + "\n"

class GoodreadsSession:
    """ Handles OAuth sessions """
    def __init__(self, client_key, client_secret, \
                 access_token=None, access_token_secret=None):
        self.session = None
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret


    def oath_start(self):
        """ Start oauth, get tokens return authorization url"""
        # Create auth service
        goodreads_service = OAuth1Service(
            consumer_key=self.client_key,
            consumer_secret=self.client_secret,
            name='goodreads',
            request_token_url='http://www.goodreads.com/oauth/request_token',
            authorize_url='http://www.goodreads.com/oauth/authorize',
            access_token_url='http://www.goodreads.com/oauth/access_token',
            base_url='http://www.goodreads.com/'
            )

        # Get tokens and authorization link
        self.request_token, self.request_token_secret = \
            goodreads_service.get_request_token(header_auth=True)

        authorize_url = goodreads_service.get_authorize_url(self.request_token)
        print 'To authorize access visit: ' + authorize_url

        # Store service for finishing
        self.goodreads_service = goodreads_service

        return authorize_url

    def oauth_finish(self):
        """ Finish creating session after user authorized access.
            save access tokens as instance members. """
        self.session = self.goodreads_service.get_auth_session(self.request_token,
                                                          self.request_token_secret)
        # TODO: Check session valid
        self.access_token = self.session.access_token
        self.access_token_secret = self.session.access_token_secret

    def oath_resume(self):
        """ Create a session when access tokens are already available """
        self.session = OAuth1Session(
                        consumer_key = self.client_key,
                        consumer_secret = self.client_secret,
                        access_token = self.access_token,
                        access_token_secret = self.access_token_secret,
                    )

    def post(self, url, data={}):
        """  """
        # Are there parameters?
        if len(data) > 0:
            url += '?'
        response = self.session.post('http://www.goodreads.com/'+url, params=data)
        if response.status_code == 201:
            data_dict = xmltodict.parse(response.content)
            return data_dict['GoodreadsResponse']
        else:
            raise Exception('Cannot create resource: %s' % response.status_code)


    def get(self, url, data={}):
        """  """
        # Are there parameters?
        if len(data) > 0:
            url += '?'
            
        response = self.session.get('https://www.goodreads.com/'+url, params=data)
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.content)
            return data_dict['GoodreadsResponse']
        else:
            raise Exception('Unable to GET: %s' % response.status_code)
