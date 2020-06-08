'''Forge URLs and utility functions'''

from . import AFWExceptions

AUTODESK_BASE_URL = "https://developer.api.autodesk.com"

TOKENFLEX_API = AUTODESK_BASE_URL+"/tokenflex/v1"
RECAP_API = AUTODESK_BASE_URL+"/photo-to-3d/v1"
AUTH_API = AUTODESK_BASE_URL+"/authentication/v1"
INFO_AUTH = AUTODESK_BASE_URL+"/userprofile/v1"
DA_API = AUTODESK_BASE_URL+"/da/us-east/v3"

# BIM360 and data management APIs are not consistent with their API urls


def checkScopes(token, endpoint_scope: str):
    '''Checks scopes before making the request.'''
    token_scope = token.scope.split()
    endpoint_scope = endpoint_scope.split()
    result =  all(elem in token_scope  for elem in endpoint_scope)
    if result:
        return True
    else:
        raise AFWExceptions.AFWError("Missing required scopes:", endpoint_scope)

def checkResponse(r):
    '''If the response raised an error, this will detect it'''
    if "code" in r and "message" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["code"], e2=r["message"]))
    elif "developerMessage" in r and "errorCode" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["errorCode"], e2=r["developerMessage"]))
    elif "code" in r and "msg" in r:
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["code"], e2=r["msg"]))
    elif "jsonapi" in r and "errors" in r: # Check for dm errors, response returns a list of errors so raise that list
        raise AFWExceptions.APIError(r["errors"])
    elif "Error" in r: # This is ReCap format... too many error formats
        raise AFWExceptions.APIError("CODE {e1} - {e2}".format(e1=r["Error"]["code"], e2=r["Error"]["msg"]))

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def allowed_kwargs_check(allowedKwgs, kwgs):
    '''Check kwargs'''
    for kwg in kwgs:
        if kwg not in allowedKwgs:
            raise AFWExceptions.AFWError("Invalid kwarg. See allowed kwargs in the docstring")

