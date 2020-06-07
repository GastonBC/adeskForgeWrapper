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
    cliId and cliSecret from the Forge app
    bimAcc and bimAccName are your B360 credentials'''
    
    def __init__(self, cliId, cliSecret, bimAccId, bimAccName):
        self.cliId = cliId
        self.cliSecret = cliSecret
        self.bimAccId = bimAccId
        self.bimAccName = bimAccName
        self.hubId = "b.{}".format(bimAccId)

    def me(self, token):
        '''Get the profile information of an authorizing end user in a 
        three-legged context.'''
        endpointUrl = INFO_AUTH+"/users/@me"
        r = requests.get(endpointUrl, headers=token.getHeader).json()
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
    getHeader<br>
    patchHeader<br>
    contentXUser<br>'''
    def __init__(self, client, r, scope, flow):
        self._cliId = client.cliId
        self._cliSecret = client.cliSecret
        self._bimAccId = client.bimAccId
        self._bimAccName = client.bimAccName
        self._hubId = client.hubId
        self._isThreeLegged = flow
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

        self._getHeader = {"Authorization":self._access_token}

        self._urlEncoded = {'Content-Type': 'application/x-www-form-urlencoded', 
                            'Authorization': self._access_token}

        self._formData = {'Content-Type': 'multipart/form-data', 
                            'Authorization': self._access_token}

        self._patchHeader = {'Content-Type': 'application/json', 
                                'Authorization': self._access_token}

        self._contentXUser = {'Content-Type': 'application/json', 
                                'Authorization': self._access_token, 
                                "x-user-id":client.bimAccId}

        self._XUser = {'Authorization':self._access_token, 
                        "x-user-id":client.bimAccId}
           
    @property
    def cliId(self):
        return self._cliId
    @property
    def cliSecret(self):
        return self._cliSecret
    @property
    def bimAccId(self):
        return self._bimAccId
    @property
    def bimAccName(self):
        return self._bimAccName
    @property
    def hubId(self):
        return self._hubId
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
    def getHeader(self):
        return self._getHeader
    @property
    def patchHeader(self):
        return self._patchHeader
    @property
    def contentXUser(self):
        return self._contentXUser
    @property
    def urlEncoded(self):
        return self._urlEncoded
    @property
    def formData(self):
        return self._formData
    @property
    def isThreeLegged(self):
        return self._isThreeLegged
    @property
    def XUser(self):
        return self._XUser

    @classmethod
    def get_2_legged_token(cls, scope, client):
        '''Gets a 2 legged token according to the scope.<br>
        Scope - The scope you aim for. <br>
        eg "account:read data:read". client_id and client_secret from the forge api web'''

        header = {"Content-Type":"application/x-www-form-urlencoded"}
        data = {"client_id":client.cliId,
                "client_secret":client.cliSecret,
                "grant_type":"client_credentials",
                "scope":"{}".format(scope)}
        endpointUrl = AUTH_API+"/authenticate"
        r = requests.post(endpointUrl, data, header).json()
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
    
        endpointUrl = AUTH_API+"/authorize"

        params = (("client_id", client.cliId), 
                  ("response_type", tokenType), 
                  ("redirect_uri", callback_URL), 
                  ("scope", scope))

        r = requests.post(endpointUrl, params=params)

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
__pdoc__['Token.getHeader'] = False
__pdoc__['Token.patchHeader'] = False
__pdoc__['Token.contentXUser'] = False