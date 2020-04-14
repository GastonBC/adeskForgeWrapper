# ----------
# Forge API exceptions
# https://forge.autodesk.com/en/docs/bim360/v1/reference/http/
# ----------

class forgeException(Exception):
    '''Base class for forge exception responses'''

class scopeException(forgeException):
    '''Class for missing scopes'''