import requests
from time import sleep
import webbrowser
from urllib.parse import urlparse, parse_qs
from .urls import AUTH_API, INFO_AUTH

from . import fpwExceptions

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
        '''Get the profile information of an authorizing end user in a three-legged context.'''
        endpointUrl = INFO_AUTH+"/users/@me"
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        print(r)

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
    def __init__(self, client, r, scope):
        if type(r) == dict:
            self.__raw = r
            self.__scope = scope
            self.__token_type = r["token_type"] or None
            self.__expires_in = r["expires_in"] or None
            self.__access_token = r["access_token"]

            self.__getHeader = {"Authorization":"Bearer {}".format(r["access_token"])}
            self.__urlEncoded = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(r["access_token"])}

            self.__formData = {'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(r["access_token"])}

            self.__patchHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r["access_token"])}
            self.__contentXUser = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r["access_token"]), "x-user-id":client.bimAccId}
        elif type(r) == str:
            self.__raw = r
            self.__scope = scope
            self.__token_type = None
            self.__expires_in = None
            self.__access_token = r

            self.__getHeader = {"Authorization":"Bearer {}".format(r)}
            self.__urlEncoded = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(r)}

            self.__formData = {'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer {}'.format(r)}

            self.__patchHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r)}
            self.__contentXUser = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r), "x-user-id":client.bimAccId}

    @property
    def raw(self):
        return self.__raw
    @property
    def scope(self):
        return self.__scope
    @property
    def token_type(self):
        return self.__token_type
    @property
    def expires_in(self):
        return self.__expires_in
    @property
    def access_token(self):
        return self.__access_token
    @property
    def getHeader(self):
        return self.__getHeader
    @property
    def patchHeader(self):
        return self.__patchHeader
    @property
    def contentXUser(self):
        return self.__contentXUser
    @property
    def urlEncoded(self):
        return self.__urlEncoded
    @property
    def formData(self):
        return self.__formData

    @classmethod
    def get2LeggedToken(cls, scope: type(str), client: Client):
        '''Gets a 2 legged token according to the scope.<br>
        Scope: The scope you aim for. <br>
        eg "account:read data:read". client_id and client_secret from the forge api web'''
        header = {"Content-Type":"application/x-www-form-urlencoded"}
        data = {"client_id":client.cliId,
                "client_secret":client.cliSecret,
                "grant_type":"client_credentials",
                "scope":"{}".format(scope)}
        endpointUrl = AUTH_API+"/authenticate"
        r = requests.post(endpointUrl, data, header).json()
        checkResponse(r)
        return cls(client, r, scope)

    @classmethod
    def get3LeggedToken(cls, scope: type(str), client: Client, callback_URL: type(str), tokenType="token"):
        '''Get a 3 legged token according to the scope.<br>
        Scope: The scope you aim for. <br>
        callback_URL: The callback url the user will be taken to after authorization. This<br>
        url must be the same callback url you used to register your Forge App.<br>
        eg "account:read data:read". client_id and client_secret from the forge api web'''
        from urllib.parse import quote

        urlClean = quote(callback_URL, safe='')
        endpointUrl = AUTH_API+"/authorize?response_type={tokType}&client_id={cliId}&redirect_uri={redirect}&scope={scope}".format(
                                                            tokType = tokenType, cliId=client.cliId, redirect=urlClean, scope=scope)

        r = requests.post(endpointUrl)
        if tokenType == "token":
            print("You will be prompted to login. Do so and copy the url you were redirected to")
            webbrowser.open(r.url, new = 0, autoraise=True)
            responseUrl = input("Copy the url you were redirected to here, entirely: ")

            o = urlparse(responseUrl)
            query = parse_qs(o.fragment)
            r={"token_type":query["token_type"][0],
            "expires_in":query["expires_in"][0],
            "access_token":query["access_token"][0]}

            return cls(client, r, scope)
        elif tokenType == "code":
            webbrowser.open(r.url, new = 0, autoraise=True)
            
        else:
            raise fpwExceptions.forgeException("Token type must be 'code' or 'token'")

def checkScopes(token: Token, endpointScope: str):
    '''Checks scopes before making the request.'''
    tokenScope = token.scope.split()
    endpointScope = endpointScope.split()
    result =  all(elem in tokenScope  for elem in endpointScope)
    if result:
        return True
    else:
        raise fpwExceptions.scopeException("Missing required scopes:", endpointScope)

def checkResponse(r):
    '''If the response raised an error, this will detect it'''
    if "code" and "message" in r:
        raise fpwExceptions.forgeException(r)
    elif "developerMessage" and "errorCode" in r:
        raise fpwExceptions.forgeException(r)
    elif "code" and "msg" in r:
        raise fpwExceptions.forgeException(r)

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