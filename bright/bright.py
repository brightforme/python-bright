import requests
import json
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from .helpers import raise_errors_on_failure


class Bright(object):
    use_ssl = True
    api_url = "http://api.brightfor.me/v1/"
    host = "api.brightfor.me"
    __version__ = '0.0.1'
    USER_AGENT = 'BRIGHT Python API Wrapper {0}'.format(__version__)

    
    def __init__(self,**kwargs):
        
        if 'client_id' not in kwargs:
            raise TypeError("At least a client_id must be provided.")

        self.host = kwargs.get('host', self.host)
        self.scheme = self.use_ssl and 'https://' or 'http://'
        self.use_ssl = kwargs.get('use_ssl', self.use_ssl)
        self.options = kwargs
        self.client_id = kwargs.get('client_id')
        self.scopes = kwargs.get('scopes')
        self._authorize_url = None

        if "access_token" in kwargs:
            self.access_token = kwargs.get("access_token")
            self.bright = OAuth2Session(self.client_id, token={
                        "access_token": self.access_token, 
                        "scope": self.scopes, 
                        "token_type": "Bearer"
                    })
            return
        if "username" in kwargs and "password" in kwargs:
            token_url = "{0}{1}/oauth/token".format(self.scheme,self.host)
            client = LegacyApplicationClient(self.client_id)
            self.bright = OAuth2Session(client=client)
            self.access_token = self.bright.fetch_token(token_url,
                                                client_id=self.client_id,
                                                username=kwargs.get("username"),
                                                password=kwargs.get("password"),
                                                scope=self.scopes,
                                                )


        

    def make_call(self,endpoint,method,payload={}):
        payload = json.dumps(payload)
        headers = {
            'User-Agent': self.USER_AGENT,
            'Accept':'application/json'
        }
        if method == 'GET':
            r = self.bright.get(self.api_url + endpoint,headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'DELETE':
            r = self.bright.delete(self.api_url + endpoint, data=payload, headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'POST':
            r = self.bright.post(self.api_url + endpoint, data=payload, headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'PUT':
            r = self.bright.put(self.api_url + endpoint, data=payload, headers=headers)
            r = raise_errors_on_failure(r)

        return r.json()
    