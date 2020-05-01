# ----------
# Wrapper for DATA MANAGEMENT API
# https://forge.autodesk.com/en/docs/data/v2/reference/http/
# ----------

import requests
from . import fpwExceptions
from .client import Client
from .client import Token
from .client import checkResponse
from .client import checkScopes
from .urls import AUTODESK_BASE_URL as BASE_URL

class Hub(object):
    __apiType = "hubs"
    def __init__(self, raw, name, hubId: str):
        self.__raw = raw
        self.__name = name
        self.__hubId = hubId

    @property
    def apiType(self):
        return self.__apiType
    @property
    def raw(self):
        return self.__raw
    @property
    def name(self):
        return self.__name
    @property
    def hubId(self):
        return self.__hubId

    @classmethod
    def hubById(cls, token, hub_id):
        '''Returns info on the hub given
        scope: data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}".format(hId=hub_id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r, r["data"]["attributes"]["name"], r["data"]["id"])

    @classmethod
    def getHubs(cls, token):
        '''Returns a collection of accessible hubs for this member.
        Scope data:read
        

        Hubs represent BIM 360 Team hubs, Fusion Team hubs (formerly known as A360 Team hubs),
        A360 Personal hubs, or BIM 360 Docs accounts. Team hubs include BIM 360 Team hubs
        and Fusion Team hubs (formerly known as A360 Team hubs). Personal hubs include A360 Personal hubs.'''
        # try:
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs"
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(h, h["attributes"]["name"], h["id"]) for h in r["data"]]
        # except:
        #     raise fpwExceptions.forgeException(r)
        # TODO NON ACCESSIBLE HUBS RETURN ERROR, HANDLE THAT

    def getProjectsByHub(self, token):
        '''Returns a list of all projects in the hub
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects".format(hId=self.hubId)
        projects = requests.get(endpointUrl,headers=token.getHeader).json()
        checkResponse(projects)
        return [Project(p, p["id"], p["attributes"]["name"], self.hubId) for p in projects["data"]]

class Project(object):
    __apiType = "projects"
    def __init__(self, raw, Id, name, hubId):
        '''TODO'''
        self.__raw = raw
        self.__Id = Id
        self.__name = name
        self.__hubId = hubId

    @property
    def apiType(self):
        return self.__apiType
    @property
    def raw(self):
        return self.__raw
    @property
    def Id(self):
        return self.__Id
    @property
    def name(self):
        return self.__name
    @property
    def hubId(self):
        return self.__hubId

    @classmethod
    def getProjectById(cls, token, hub: Hub, p_id):
        '''Returns a specific project by id
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}".format(hId=hub.hubId, pId=p_id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r, r["data"]["id"], r["data"]["attributes"]["name"], r["data"]["relationships"]["hub"]["data"]["id"])

    def getHubFromProject(self, token):
        '''Returns a specific hub from current project
        Scope data:read'''
        checkScopes(token, "data:read")
        return Hub.hubById(token, self.hubId)

    def getTopFolders(self, token):
        '''Returns the details of the highest level folders the user has access to for a given project. 
        The user must have at least read access to the folders.
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}/topFolders".format(hId=self.hubId, pId=self.Id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [Folder.folderById(token, self, tF["id"]) for tF in r["data"]]

class Folder(object):
    __apiType = "folders"
    def __init__(self, raw, Id, name, hidden):
        '''Base folder class'''
        self.__raw = raw
        self.__Id = Id
        self.__name = name
        self.__hidden = hidden

    @property
    def apiType(self):
        return self.__apiType
    @property
    def Id(self):
        return self.__Id
    @property
    def name(self):
        return self.__name
    @property
    def hidden(self):
        return self.__hidden

    @classmethod
    def folderById(cls, token: Token, project: Project, folderId):
        '''Returns a specific folder by id
        Scope data:read
        p_id: the project id in which the folder is contained
        f_id: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=project.Id, f_id=folderId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r, r["data"]["id"], r["data"]["attributes"]["name"], r["data"]["attributes"]["hidden"])

    @classmethod
    def CreateFolder(cls, token: Token, project: Project, folderId):
        '''Returns a specific folder by id
        Scope data:read
        p_id: the project id in which the folder is contained
        f_id: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=project.Id, f_id=folderId)
        r = requests.get(endpointUrl ,headers=token.getHeader).json()
        checkResponse(r)
        return cls(r, r["data"]["id"], r["data"]["attributes"]["name"], r["data"]["attributes"]["hidden"])


# TODO SPLIT REQUEST LINE. MOVE URL TO A NEW VARIABLE URL. BETTER READABILITY. EXAMPLE
        # endpointUrl = "https://developer.api.autodesk.com/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=project.Id, f_id=folderId)
        # r = requests.get(url, headers=token.getHeader).json()


# TODO FAR IN THE FUTURE: OBJECT CLASS INHERITANCE: HUB > PROJECT > FOLDER > ITEM. THAT WAY WE CAN USE ATTRIBUTE INHERITED
#      INVESTIGATE PROS N CONS OF THIS
#      https://stackoverflow.com/questions/8853966/the-inheritance-of-attributes-using-init

# TODO LEFT
# Projects
# GET projects/:project_id/downloads/:download_id
# GET projects/:project_id/jobs/:job_id
# POST projects/:project_id/downloads
# POST projects/:project_id/storage

# Folders
# GET projects/:project_id/folders/:folder_id/contents
# GET projects/:project_id/folders/:folder_id/parent
# GET projects/:project_id/folders/:folder_id/refs
# GET projects/:project_id/folders/:folder_id/relationships/links
# GET projects/:project_id/folders/:folder_id/relationships/refs
# GET projects/:project_id/folders/:folder_id/search
# POST projects/:project_id/folders
# POST projects/:project_id/folders/:folder_id/relationships/refs
# PATCH projects/:project_id/folders/:folder_id

# Items
# GET projects/:project_id/items/:item_id
# GET projects/:project_id/items/:item_id/parent
# GET projects/:project_id/items/:item_id/refs
# GET projects/:project_id/items/:item_id/relationships/links
# GET projects/:project_id/items/:item_id/relationships/refs
# GET projects/:project_id/items/:item_id/tip
# GET projects/:project_id/items/:item_id/versions
# POST projects/:project_id/items
# POST projects/:project_id/items/:item_id/relationships/refs
# PATCH projects/:project_id/items/:item_id

# Versions
# GET projects/:project_id/versions/:version_id
# GET projects/:project_id/versions/:version_id/downloadFormats
# GET projects/:project_id/versions/:version_id/downloads
# GET projects/:project_id/versions/:version_id/item
# GET projects/:project_id/versions/:version_id/refs
# GET projects/:project_id/versions/:version_id/relationships/links
# GET projects/:project_id/versions/:version_id/relationships/refs
# POST projects/:project_id/versions
# POST projects/:project_id/versions/:version_id/relationships/refs
# PATCH projects/:project_id/versions/:version_id

# Commands
# CheckPermission
# ListRefs
# ListItems
# CreateFolder
# PublishModel
# GetPublishModelJob

# OSS
# Buckets
# POST buckets
# GET buckets
# GET buckets/:bucketKey/details
# DELETE buckets/:bucketKey

# Objects
# PUT buckets/:bucketKey/objects/:objectName
# PUT buckets/:bucketKey/objects/:objectName/resumable
# GET buckets/:bucketKey/objects/:objectName/status/:sessionId
# GET buckets/:bucketKey/objects
# GET buckets/:bucketKey/objects/:objectName/details
# GET buckets/:bucketKey/objects/:objectName
# POST buckets/:bucketKey/objects/:objectName/signed
# PUT signedresources/:id
# PUT signedresources/:id/resumable
# GET signedresources/:id
# DELETE signedresources/:id
# PUT buckets/:bucketKey/objects/:objectName/copyto/:newObjectName
# DELETE buckets/:bucketKey/objects/:objectName