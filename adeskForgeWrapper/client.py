import requests
import fpwExceptions

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

class Token(object):
    '''A class representing the token'''
    def __init__(self, scope: type(str), client: Client):
        '''Gets a 2 legged token according to the scope. scope: The scope you aim for. 
        eg "account:read data:read". client_id and client_secret from the forge api web'''
        header = {"Content-Type":"application/x-www-form-urlencoded"}
        data = {"client_id":client.cliId,
                "client_secret":client.cliSecret,
                "grant_type":"client_credentials",
                "scope":"{}".format(scope)}
        r = requests.post("https://developer.api.autodesk.com/authentication/v1/authenticate", data, header).json()
        checkResponse(r)
        self.__raw = r
        self.__scope = scope
        self.__token_type = r["token_type"]
        self.__expires_in = r["expires_in"]
        self.__access_token = r["access_token"]

        self.__getHeader = {"Authorization":"Bearer {}".format(r["access_token"])}
        self.__patchHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r["access_token"])}
        self.__contentXUser = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(r["access_token"]), "x-user-id":client.bimAccId}

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

    @classmethod
    def get3LeggedToken(cls, scope: type(str), client: Client):
        r = requests.get("https://developer.api.autodesk.com/authentication/v1/authorize?response_type=code&client_id={cliId}&redirect_uri=https%3A%2F%2Fdashboard.archsourcing.com&scope={scope}".format(cliId= client.cliId, scope= scope))
        print(r.text)
def checkScopes(token: Token, endpointScope: str):
    tokenScope = token.scope.split()
    endpointScope = endpointScope.split()
    result =  all(elem in tokenScope  for elem in endpointScope)
    if result:
        return True
    else:
        raise fpwExceptions.scopeException("Missing required scopes:", endpointScope)

def checkResponse(r):
    if "code" and "message" in r:
        raise fpwExceptions.forgeException(r)
    elif "developerMessage" and "errorCode" in r:
        raise fpwExceptions.forgeException(r)