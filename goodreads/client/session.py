from rauth.service import OAuth1Service, OAuth1Session

class GoodreadsSession:
    """ Handles OAuth sessions """
    def __init__(self, client_key, client_secret, access_token=None, access_token_secret=None):
        self.session = None
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret


    def oath_initialize(self):
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
        request_token, request_token_secret = goodreads_service.get_request_token(
                                        header_auth=True)
        authorize_url = goodreads_service.get_authorize_url(request_token)
        print 'To authorize access visit: ' + authorize_url

        # Store service for continuation
        self.goodreads_service = goodreads_service
        
        return authorize_url

    def oath_complete(self):
        """ Finish creating session after user authorized access """
        self.session = goodreads_service.get_auth_session(request_token,
                                                          request_token_secret)
        # TODO: Check session valid

        self.acceess_token = session.access_token
        self.access_token_secret = session.access_token_secret

    def oath_resume(self):
        """ Create a session when access tokens are already available """
        self.session = OAuth1Session(
                        consumer_key = self.client_key,
                        consumer_secret = self.client_secret,
                        access_token = self.acceess_token,
                        access_token_secret = self.access_token_secret,
                    )   

    def post(self, url, data=None):
        """  """
        response = self.session.post('http://www.goodreads.com/'+url, data)

        #TODO: Handle response


    def get(self, url, data=None):
        """  """
        response = self.session.post('http://www.goodreads.com/'+url, data)

        #TODO: Handle response

