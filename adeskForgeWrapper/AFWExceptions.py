# ----------
# Forge API exceptions
# https://forge.autodesk.com/en/docs/bim360/v1/reference/http/
# ----------

class AFWError(Exception):
    '''Base class for AFW exceptions'''

class APIError(Exception):
    '''Base class for API response exceptions'''