import requests
import json
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from .helpers import raise_errors_on_failure


class Bright(object):
    use_ssl = True
    api_url = "https://api.brightfor.me/v1/"
    host = "api.brightfor.me"
    __version__ = '0.0.1'
    USER_AGENT = 'python-bright v{0}'.format(__version__)

    
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

    def make_request(self,endpoint,method,payload=None,params={}):
        if payload:
            payload = json.dumps(payload)

        headers = {
            'User-Agent': self.USER_AGENT,
            'Accept':'application/json',
            'Content-Type':'application/json'
        }
        if method == 'GET':
            r = self.bright.get(self.api_url + endpoint, 
                                params=params,
                                headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'DELETE':
            r = self.bright.delete(self.api_url + endpoint, 
                                    params=params, 
                                    data=payload, 
                                    headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'POST':
            r = self.bright.post(self.api_url + endpoint, 
                                params=params, 
                                data=payload, 
                                headers=headers)
            r = raise_errors_on_failure(r)
        if method == 'PUT':
            r = self.bright.put(self.api_url + endpoint, 
                                params=params, 
                                data=payload, 
                                headers=headers)
            r = raise_errors_on_failure(r)

        return r.json()

    def me(self):
        return self.make_request('me','GET')

    def my_collections(self):
        return self.make_request('me/collections','GET')

    def my_artworks(self):
        return self.make_request('me/artworks','GET')

    def me_notifications(self):
        return self.make_request('me/notifications','GET')

    def update_me(self, data={}):
        return self.make_request('me','PUT',payload=data)

    def get_artwork(self, artwork_id):
        uri = "artworks/{0}".format(artwork_id)
        return self.make_request(uri,'GET')

    def get_all_artworks(self,per_page=None,page=None):

        params = {
            "page":page,
            "per_page": per_page or 10
            }

        return self.make_request('artworks/','GET', params=params)

    def update_artwork(self,artwork_id, data={}):
        uri = 'artworks/{0}'.format(artwork_id)
        return self.make_request(uri,'PUT',payload=data)

    def delete_artwork(self,artwork_id):
        uri = 'artworks/{0}'.format(artwork_id)
        return self.make_request(uri,'DELETE')

    def create_collection(self, name, description):
        data = {
            'name':name,
            'description':description
        }
        return self.make_request("collections/","POST",payload=data)

    def get_collection(self, collection_id):
        uri = "collections/{0}".format(collection_id)
        return self.make_request(uri,'GET')

    def get_all_collections(self,per_page=None,page=None):

        params = {
            "page":page,
            "per_page": per_page or 10
            }

        return self.make_request('collections/','GET', params=params)

    def update_collection(self, collection_id, data={}):
        uri = "collections/{0}".format(collection_id)
        return self.make_request(uri,'PUT', payload=data)

    def delete_collection(self, collection_id):
         uri = "collections/{0}".format(collection_id)
         return self.make_request(uri,'DELETE')
    
    def add_to_collection(self, collection_id, artwork_id):
        uri = "collections/{0}/artworks/".format(collection_id)
        data = {
            "artwork":artwork_id
        }
        return self.make_request(uri,'POST',payload=data)

    def remove_from_collection(self, collection_id, artwork_id):
        uri = "collections/{0}/artworks/".format(collection_id)
        data = {
            "artwork_id_or_slug":artwork_id
        }
        return self.make_request(uri,'DELETE',payload=data)

    def like_collection(self, collection_id):
        uri = "collections/{0}/like".format(collection_id)
        return self.make_request(uri,'POST')

    def unlike_collection(self, collection_id):
        uri = "collections/{0}/unlike".format(collection_id)
        return self.make_request(uri,'POST')

    def get_user(self, user_id_or_screenname):
        uri = "users/{0}".format(user_id_or_screenname)
        return self.make_request(uri, 'GET')

    def follow_user(self, user_id_or_screenname):
        uri = "users/{0}/follow".format(user_id_or_screenname)
        return self.make_request(uri, 'POST')

    def unfollow_user(self, user_id_or_screenname):
        uri = "users/{0}/unfollow".format(user_id_or_screenname)
        return self.make_request(uri, 'POST')
    