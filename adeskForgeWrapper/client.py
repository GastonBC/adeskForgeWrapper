'''Client information and token requests'''
import requests

from time import sleep

from .utils import AUTH_API
from .utils import INFO_AUTH
from .utils import checkResponse
from .utils import checkScopes

from . import AFWExceptions

class Client(object):
    '''A class containing information from the user's end
    client_id and client_secret from the Forge app
    bimAcc and bim_account_name are your B360 credentials'''
    
    def __init__(self, client_id, client_secret, bim_account_id, bim_account_name):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bim_account_id = bim_account_id
        self.bim_account_name = bim_account_name
        self.hub_id = "b.{}".format(bim_account_id)

    def me(self, token):
        '''Get the profile information of an authorizing end user in a 
        three-legged context.'''
        endpoint_url = INFO_AUTH+"/users/@me"
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        print(r) # TODO Maybe can return a DM.User object

# TODO new defs: getExpirationTime, renew
class Token(object):
    '''A class representing the token.<br>
    raw<br>
    scope<br>
    token_type<br>
    expires_in<br>
    access_token<br>
    get_header<br>
    patchHeader<br>
    contentXUser<br>'''
    def __init__(self, client, r, scope, flow):
        self._client_id = client.client_id
        self._client_secret = client.client_secret
        self._bim_account_id = client.bim_account_id
        self._bim_account_name = client.bim_account_name
        self._hub_id = client.hub_id
        self._is_three_legged = flow
        self._scope = scope

        if type(r) == dict:
            self._raw = r
            
            self._token_type = r.get("token_type", None)
            self._expires_in = r.get("expires_in", None)
            self._access_token = 'Bearer {}'.format(r.get("access_token"))

        elif type(r) == str:
            self._raw = r
            self._token_type = None
            self._expires_in = None
            self._access_token = 'Bearer {}'.format(r)
       
    @property
    def client_id(self):
        return self._client_id
    @property
    def client_secret(self):
        return self._client_secret
    @property
    def bim_account_id(self):
        return self._bim_account_id
    @property
    def bim_account_name(self):
        return self._bim_account_name
    @property
    def hub_id(self):
        return self._hub_id
    @property
    def raw(self):
        return self._raw
    @property
    def scope(self):
        return self._scope
    @property
    def token_type(self):
        return self._token_type
    @property
    def expires_in(self):
        return self._expires_in
    @property
    def access_token(self):
        return self._access_token
    @property
    def get_header(self):
        header = {"Authorization":self._access_token}
        return header
    @property
    def patch_header(self):
        header = {'Content-Type': 'application/json', 
                  'Authorization': self._access_token}
        return header
    @property
    def content_x_user(self):
        header = {'Content-Type': 'application/json', 
                  'Authorization': self._access_token, 
                  'x-user-id':self._bim_account_id}
        return header
    @property
    def url_encoded(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded', 
                  'Authorization': self._access_token}
        return header
    @property
    def form_data(self):
        header = {'Content-Type': 'multipart/form-data', 
                  'Authorization': self._access_token}
        return header
    @property
    def x_user(self):
        header = {'Authorization':self._access_token, 
                  'x-user-id':self._bim_account_id}
        return header
    @property
    def is_three_legged(self):
        return self._is_three_legged

    @classmethod
    def get_2_legged_token(cls, scope, client):
        '''Gets a 2 legged token according to the scope.<br>
        Scope - The scope you aim for. <br>
        eg "account:read data:read". client_id and client_secret from the forge api web'''

        header = {"Content-Type":"application/x-www-form-urlencoded"}
        data = {"client_id":client.client_id,
                "client_secret":client.client_secret,
                "grant_type":"client_credentials",
                "scope":"{}".format(scope)}
        endpoint_url = AUTH_API+"/authenticate"
        r = requests.post(endpoint_url, data, header).json()
        checkResponse(r)
        return cls(client, r, scope, False)

    @classmethod
    def get_3_legged_token(cls, scope, client, callback_URL, tokenType="token"):
        '''Get a 3 legged token according to the scope.<br>
        Scope - The scope you aim for. <br>
        callback_URL: The callback url the user will be taken to after authorization.<br>
        url must be the same callback url you used to register your Forge App.<br>
        eg "account:read data:read". client_id and client_secret from the forge api web'''

        if  "http://" not in callback_URL and "https://" not in callback_URL:
            raise AFWExceptions.AFWError("Protocol missing in callback_URL (http:// or https://)")
        
        import urllib.parse
        import webbrowser
    
        endpoint_url = AUTH_API+"/authorize"

        params = (("client_id", client.client_id), 
                  ("response_type", tokenType), 
                  ("redirect_uri", callback_URL), 
                  ("scope", scope))

        r = requests.post(endpoint_url, params=params)

        checkResponse(r)
        if tokenType == "token":
            print("You will be prompted to login. Do so and copy the url you were redirected to")
            webbrowser.open(r.url, new = 0, autoraise=True)
            responseUrl = input("Copy the url you were redirected to here, entirely: ")

            o = urllib.parse.urlparse(responseUrl)
            query = urllib.parse.parse_qs(o.fragment)
            r={"token_type":query["token_type"][0],
            "expires_in":query["expires_in"][0],
            "access_token":query["access_token"][0]}

            return cls(client, r, scope, True)
        elif tokenType == "code":
            pass # TODO
            
            
        else:
            raise AFWExceptions.AFWError("Token type must be 'code' or 'token'")



# pdocs stuff
__pdoc__ = {}
__pdoc__['Token.raw'] = False
__pdoc__['Token.raw'] = False
__pdoc__['Token.scope'] = False
__pdoc__['Token.token_type'] = False
__pdoc__['Token.expires_in'] = False
__pdoc__['Token.access_token'] = False
__pdoc__['Token.get_header'] = False
__pdoc__['Token.patchHeader'] = False
__pdoc__['Token.contentXUser'] = False