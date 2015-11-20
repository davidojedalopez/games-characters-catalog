# Implementation based on OAuth Authentication with Flask tutorial 
# from Miguel Grinberg (http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)

import random, string
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
import json
import urllib2

class OAuthSignIn(object):
    """
    Base class under which the provider specific implementations will be written.
    """
    providers = None

    def __init__(self, provider_name):
        """
        Constructor to initialize provider's name, application ID and application secret.
        """
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class GoogleSignIn(OAuthSignIn):
    """
    Sub-Class of OAuthSignIn for Google sign in.  
    """
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        # Get the URL's for the OAuth2Service object for Rauth from Google well-known configuration page
        googleinfo = urllib2.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        # Create the service object using OAuth2Service
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google_params.get("authorization_endpoint"),
            access_token_url=google_params.get('token_endpoint'),
            base_url=google_params.get('userinfo_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        """
        Provider passes a verification token that the application can use to contact
        the provider's API.

        return: User data in tuple format
        """
        # In this case, the 'code' is the token
        if 'code' not in request.args:
            return None, None, None

        # Use the token to get the oauth_session object and request user information
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads
        )

        me = oauth_session.get('').json()

        # Preppend provider name to social ID random generated string 
        social_id = 'google$' + "".join(random.choice(string.lowercase) for i in range(15))
        username = me.get('email').split("@")[0]
        email = me.get('email')

        return social_id, username, email

