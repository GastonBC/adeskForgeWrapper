'''AUTODESK'S FORGE URLS'''

from . import AFWExceptions

AUTODESK_BASE_URL = "https://developer.api.autodesk.com"

TOKENFLEX_API = AUTODESK_BASE_URL+"/tokenflex/v1"
RECAP_API = AUTODESK_BASE_URL+"/photo-to-3d/v1"
AUTH_API = AUTODESK_BASE_URL+"/authentication/v1"
INFO_AUTH = AUTODESK_BASE_URL+"/userprofile/v1"
# BIM360 and data management APIs are not consistent with their API urls


def checkScopes(token, endpointScope: str):
    '''Checks scopes before making the request.'''
    tokenScope = token.scope.split()
    endpointScope = endpointScope.split()
    result =  all(elem in tokenScope  for elem in endpointScope)
    if result:
        return True
    else:
        raise AFWExceptions.AFWError("Missing required scopes:", endpointScope)

def checkResponse(r):
    '''If the response raised an error, this will detect it'''
    if "code" in r and "message" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["code"], e2=r["message"]))
    elif "developerMessage" in r and "errorCode" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["errorCode"], e2=r["developerMessage"]))
    elif "code" in r and "msg" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["code"], e2=r["msg"]))
    elif "jsonapi" in r and "errors" in r: # Check for DM errors, response returns a list of errors so raise that list
        raise AFWExceptions.APIError(r["errors"])
    elif "Error" in r: # This is ReCap format... too many error formats
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["Error"]["code"], e2=r["Error"]["msg"]))

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

