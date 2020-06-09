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
import json

class ForgeApps(object):
    def __init__(self):
        pass

    @classmethod
    def get_nickname(cls, token, id):
        '''Return the given Forge app’s nickname.<br><br>

        If the app has no nickname, this route will return its id.'''
        endpoint_url = DA_API+"/forgeapps/{id}".format(id=id)
        checkScopes(token, "code:all")
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [cls()]

    @classmethod
    def create_nickname(cls, token, nickname):
        '''Creates/updates the nickname for the current Forge app. The nickname is used 
        as a clearer alternative name when identifying AppBundles and Activities, as 
        compared to using the Forge app ID. Once you have defined a nickname, it MUST be 
        used instead of the Forge app ID.<br><br>
        
        The new nickname cannot be in use by any other Forge app.<br><br>

        The Forge app cannot have any data when this endpoint is invoked. Use 
        the ‘delete_data(token)’ function (cautiously!!!) to remove all data from 
        this Forge app. ‘delete_data(token)’ is also the only way to remove 
        the nickname.'''

        #From docs: id must be “me” for the call to succeed.
        endpoint_url = DA_API+"/forgeapps/me"
        checkScopes(token, "code:all")

        data = { "nickname":nickname }
        data = json.dumps(data, ensure_ascii=True)

        r = requests.patch(endpoint_url, headers=token.patch_header, data=data)
        checkResponse(r)
        if r.status_code == 200:
            return True
        else:
            return False

    def delete_data(self, token):
        '''Delete all data associated with the given Forge app.<br><br>

        ALL Design Automation appbundles and activities are DELETED.<br><br>

        This may take up to 2 minutes. During this time the app will not be able 
        to make successful requests.'''

        #From docs: id must be “me” for the call to succeed.
        endpoint_url = DA_API+"/forgeapps/me"
        checkScopes(token, "code:all")

        r = requests.delete(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return True

class AppBundles(object):
    def __init__(self):
        pass

    def register_appbundle(self, token, bundle_name, engine, engine_version, description):
        endpoint_url = DA_API+"/appbundles"
        checkScopes(token, "code:all")

        engine = "{}+{}".format(engine, engine_version)

        data = {
            "id": bundle_name,
            "engine": engine,
            "description": description
        }
        data = json.dumps(data, ensure_ascii=True)

        r = requests.post(endpoint_url, headers=token.patch_header, data=data)
        checkResponse(r)
        print(r["uploadParameters"]["endpointURL"])

        return True


class Engines(object):
    def __init__(self, rawDict):
        self._raw = rawDict
    

    @property
    def raw(self):
        return self._raw
    @property
    def name(self):
        _id = self._raw.get("id", None)
        _parts = _id.split("+")
        _names = _parts[0].split(".")
        return _names[1]
    @property
    def product_version(self):
        return self._raw.get("productVersion", None)
    @property
    def description(self):
        return self._raw.get("description", None)
    @property
    def version(self):
        return self._raw.get("version", None)
    @property
    def id(self):
        return self._raw.get("id", None)

    @staticmethod
    def get_engine_health(token, engine):
        '''Gets the health status by Engine or for all Engines (Inventor, AutoCAD ...).'''
        endpoint_url = DA_API + "/health/{eng}".format(eng=engine)
        checkScopes(token, "code:all")
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return r["Status"]

    @staticmethod
    def get_engines(token):
        '''Lists all available Engines.'''
        endpoint_url = DA_API+"/engines"
        checkScopes(token, "code:all")
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        
        return r["data"]

    @classmethod
    def engine_by_id(cls, token, id):
        '''Gets the details of the specified Engine. Note that the {id} parameter must be 
        a QualifiedId (owner.name+label).'''

        endpoint_url = DA_API+"/engines/{id}".format(id = id)
        checkScopes(token, "code:all")

        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return cls(r)

    def health(self, token):
        status = self.get_engine_health(token, self.name)
        return status


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

__pdoc__ = {}
__pdoc__['Engines.raw'] = False
__pdoc__['Engines.productVersion'] = False
__pdoc__['Engines.description'] = False
__pdoc__['Engines.version'] = False
__pdoc__['Engines.id'] = False