# ----------
# Wrapper for DESIGN AUTOMATION API
# https://forge.autodesk.com/en/docs/design-automation/v3/reference/http/
# ----------
'''Module for the Design Automation API'''
import requests

from . import AFWExceptions
from . import client
from .utils import checkScopes
from .utils import checkResponse
from . import utils
from .utils import DA_API

class ForgeApps(object):
    def __init__(self):
        pass

    @classmethod
    def get_nickname(cls, token, id):
        '''Return the given Forge app’s nickname.<br><br>

        If the app has no nickname, this route will return its id.'''
        endpointUrl = DA_API+"forgeapps/{id}".format(id=id)
        checkScopes(token, "code:all")
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls()]

    @classmethod
    def create_nickname(cls, token, nickname):
        '''Creates/updates the nickname for the current Forge app. The nickname is used 
        as a clearer alternative name when identifying AppBundles and Activities, as 
        compared to using the Forge app ID. Once you have defined a nickname, it MUST be 
        used instead of the Forge app ID..<br><br>
        
        The new nickname cannot be in use by any other Forge app.<br><br>

        The Forge app cannot have any data when this endpoint is invoked. Use 
        the ‘DELETE /forgeapps/me’ endpoint (cautiously!!!) to remove all data from 
        this Forge app. ‘DELETE /forgeapps/me’ is also the only way to remove 
        the nickname.'''

        #From docs: id must be “me” for the call to succeed.
        endpointUrl = DA_API+"forgeapps/{id}".format(id="me")
        checkScopes(token, "code:all")

        data = { "nickname": nickname }

        r = requests.patch(endpointUrl, headers=token.getHeader, data=data).json()
        checkResponse(r)
        return [cls()]

    def delete_data(self, token):
        '''Delete all data associated with the given Forge app.<br><br>

        ALL Design Automation appbundles and activities are DELETED.<br><br>

        This may take up to 2 minutes. During this time the app will not be able 
        to make successful requests.'''

        #From docs: id must be “me” for the call to succeed.
        endpointUrl = DA_API+"forgeapps/{id}".format(id="me")
        checkScopes(token, "code:all")

        r = requests.delete(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return True



# HTTP Specification
# Activities
# GET activities
# POST activities
# GET activities/:id/aliases/:aliasId
# DELETE activities/:id/aliases/:aliasId
# PATCH activities/:id/aliases/:aliasId
# GET activities/:id/aliases
# POST activities/:id/aliases
# GET activities/:id
# DELETE activities/:id
# GET activities/:id/versions
# POST activities/:id/versions
# GET activities/:id/versions/:version
# DELETE activities/:id/versions/:version
# AppBundles
# GET appbundles
# POST appbundles
# GET appbundles/:id/aliases/:aliasId
# DELETE appbundles/:id/aliases/:aliasId
# PATCH appbundles/:id/aliases/:aliasId
# GET appbundles/:id/aliases
# POST appbundles/:id/aliases
# GET appbundles/:id
# DELETE appbundles/:id
# GET appbundles/:id/versions
# POST appbundles/:id/versions
# GET appbundles/:id/versions/:version
# DELETE appbundles/:id/versions/:version
# Engines
# GET engines
# GET engines/:id
# ForgeApps
# GET forgeapps/:id
# DELETE forgeapps/:id
# PATCH forgeapps/:id
# Health
# GET health/:engine
# ServiceLimits
# GET servicelimits/:owner
# PUT servicelimits/:owner
# Shares
# GET shares
# WorkItems
# GET workitems/:id
# DELETE workitems/:id
# POST workitems
# POST workitems/batch