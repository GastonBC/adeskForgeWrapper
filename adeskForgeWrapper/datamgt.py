'''Module for the Data Management API'''
# ----------
# Wrapper for DATA MANAGEMENT API
# https://forge.autodesk.com/en/docs/data/v2/reference/http/
# ----------

# Properties in this API come in different formats, so we can't make use of __init__(self, rawDict) to
# get all the properties, instead, props are defined by __init__ parameters (self, raw, name, hubId)
import requests

from . import AFWExceptions
from .client import Client
from .client import Token
from .client import checkResponse
from .client import checkScopes

from .utils import AUTODESK_BASE_URL as BASE_URL

class Hub(object):
    __apiType = "hubs"
    def __init__(self, rawDict):
        self.__raw = rawDict

    @property
    def apiType(self):
        return self.__apiType
    @property
    def raw(self):
        return self.__raw
    @property
    def type(self):
        return self.__raw.get("type", None)
    @property
    def hubId(self):
        return self.__raw.get("id", None)
    @property
    def name(self):
        return self.__raw["attributes"].get("name", None)
    @property
    def region(self):
        return self.__raw["attributes"].get("region", None)

    @classmethod
    def hubById(cls, token, hub_id):
        '''Returns info on the hub give<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}".format(hId=hub_id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def get_hubs(cls, token):
        '''Returns a collection of accessible hubs for this member.<br>
        Scope - data:read<br><br>
        
        Hubs represent BIM 360 Team hubs, Fusion Team hubs (formerly known as A360 Team hubs),
        A360 Personal hubs, or BIM 360 Docs accounts.<br>
        Team hubs include BIM 360 Team hubs and Fusion Team hubs (formerly known as A360 Team hubs). Personal hubs include A360 Personal hubs.'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs"
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(h) for h in r["data"]]

    def get_projects(self, token):
        '''Returns a list of all projects in the hub<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects".format(hId=self.hubId)
        projects = requests.get(endpointUrl,headers=token.getHeader).json()
        checkResponse(projects)
        return [Project(p) for p in projects["data"]]

    def project_by_id(self, token, projectId):
        '''Returns a specific project by id
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}".format(hId=self.hubId, pId=projectId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return Project(r["data"])

class Project(object):
    __apiType = "projects"
    def __init__(self, rawDict):
        '''TODO'''
        self.__raw = rawDict

    @property
    def id(self):
        return self.__raw.get("id", None)
    @property
    def raw(self):
        return self.__raw
    @property
    def apiType(self):
        return self.__apiType
    @property
    def name(self):
        return self.__raw["attributes"].get("name", None)
    @property
    def hubId(self):
        return self.__raw["relationships"]["hub"]["data"].get("id", None)

    @classmethod
    def project_by_id(cls, token, hubId , pId):
        '''Returns a specific project by id
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}".format(hId=hubId, pId=pId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r["data"])

    def get_hub(self, token):
        '''Returns a specific hub from current project
        Scope data:read'''
        checkScopes(token, "data:read")
        return Hub.hubById(token, self.hubId)

    def top_folders(self, token):
        '''Returns the details of the highest level folders the user has access to for a given project. 
        The user must have at least read access to the folders.
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}/topFolders".format(hId=self.hubId, pId=self.id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [Folder(tF, self.id) for tF in r["data"]]

class Folder(object):
    __apiType = "folders"
    def __init__(self, rawDict, projectId):
        '''Base folder class'''
        self.__raw = rawDict
        self.__parentProjectId = projectId
    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__raw.get("id", None)
    @property
    def name(self):
        return self.__raw["attributes"].get("name", None)
    @property
    def displayName(self):
        return self.__raw["attributes"].get("displayName", None)
    @property
    def createTime(self):
        return self.__raw["attributes"].get("createTime", None)
    @property
    def createUserId(self):
        return self.__raw["attributes"].get("createUserId", None)
    @property
    def createUserName(self):
        return self.__raw["attributes"].get("createUserName", None)
    @property
    def lastModifiedTime(self):
        return self.__raw["attributes"].get("lastModifiedTime", None)
    @property
    def lastModifiedUserId(self):
        return self.__raw["attributes"].get("lastModifiedUserId", None)
    @property
    def lastModifiedUserName(self):
        return self.__raw["attributes"].get("lastModifiedUserName", None)
    @property
    def objectCount(self):
        return self.__raw["attributes"].get("objectCount", None)
    @property
    def hidden(self):
        return self.__raw["attributes"].get("hidden", None)
    @property
    def parentProjectId(self):
        return self.__parentProjectId

    @classmethod
    def folder_by_id(cls, token: Token, projectId, folderId):
        '''Returns a specific folder by id
        Scope data:read
        projectId: the project id in which the folder is contained
        folderId: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=projectId, f_id=folderId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r["data"], projectId)


    def create_folder(self, token: Token, project: Project, folderId):
        '''Returns a specific folder by id
        Scope data:read
        p_id: the project id in which the folder is contained
        f_id: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=self.parentProjectId, f_id=self.id)
        r = requests.get(endpointUrl ,headers=token.getHeader).json()
        checkResponse(r)
        return Folder(r["data"], self.parentProjectId)

    def get_contents(self, token, projectId):
        '''Returns a collection of items and folders within a folder. Items represent word documents, 
        fusion design files, drawings, spreadsheets, etc.<br>

        Notes:<br><br>

        The tip version for each item resource is included by default in the included array of the payload'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{pId}/folders/{fId}/contents".format(pId=projectId, fId=self.id)
        if token.isThreeLegged:
            r = requests.get(endpointUrl ,headers=token.getHeader).json()
        elif token.isThreeLegged is False:
            r = requests.get(endpointUrl ,headers=token.XUser).json()
        checkResponse(r)
        results = []
        for res in r["data"]:
            if res["type"] == "folders":
                results.append(Folder(res, self.parentProjectId))
            elif res["type"] == "items":
                results.append(Item(res, self.parentProjectId))
            elif res["type"] == "versions":
                results.append(Version(res, self.parentProjectId))
        return results

class Item(object):
    def __init__(self, rawDict, parentProjectId):
        self.__raw = rawDict
        self.__parentProjectId = parentProjectId
    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__raw.get("id", None)
    @property
    def displayName(self):
        return self.__raw["attributes"].get("displayName", None)
    @property
    def createUserId(self):
        return self.__raw["attributes"].get("createUserId", None)
    @property
    def createUserName(self):
        return self.__raw["attributes"].get("createUserName", None)
    @property
    def lastModifiedUserId(self):
        return self.__raw["attributes"].get("lastModifiedUserId", None)
    @property
    def lastModifiedUserName(self):
        return self.__raw["attributes"].get("lastModifiedUserName", None)
    @property
    def lastModifiedTime(self):
        return self.__raw["attributes"].get("lastModifiedTime", None)
    @property
    def createTime(self):
        return self.__raw["attributes"].get("createTime", None)
    @property
    def hidden(self):
        return self.__raw["attributes"].get("hidden", None)
    @property
    def parentFolderId(self):
        return self.__raw["relationships"]["parent"]["data"].get("id", None)
    @property
    def parentProjectId(self):
        return self.__parentProjectId

    @classmethod
    def item_by_id(cls, token, projectId, itemId):
        '''Retrieves metadata for a specified item. 
        Items represent word documents, fusion design files, drawings, spreadsheets, etc.<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{pId}/items/{itemId}".format(pId=projectId, itemId=itemId)
        r = requests.get(endpointUrl, headers=token.XUser).json()
        checkResponse(r)
        return cls(r, projectId)
    
    def get_versions(self, token):
        '''Retrieves metadata for a specified item. 
        Items represent word documents, fusion design files, drawings, spreadsheets, etc.<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{pId}/items/{itemId}/versions".format(pId=self.parentProjectId, itemId=self.id)
        r = requests.get(endpointUrl, headers=token.XUser).json()
        checkResponse(r)
        return [Version(v, self.parentProjectId) for v in r["data"]]


    def get_tip_versions(self, token):
        '''Returns the “tip” version for the given item.<br>
        Multiple versions of a resource item can be uploaded in a project. The tip version is the most recent one.<br>
        Scope - data:read'''
        # TODO Optional filter parameters
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{pId}/items/{itemId}/tip".format(pId=self.parentProjectId, itemId=self.id)
        r = requests.get(endpointUrl, headers=token.XUser).json()
        checkResponse(r)
        return Version(r, self.parentProjectId)

class Version(object):
    def __init__(self, rawDict, parentProjectId):
        self.__raw = rawDict
        self.__parentProjectId = parentProjectId

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__raw.get("id", None)
    @property
    def name(self):
        return self.__raw["attributes"].get("name", None)
    @property
    def displayName(self):
        return self.__raw["attributes"].get("displayName", None)     
    @property
    def createTime(self):
        return self.__raw["attributes"].get("createTime", None)      
    @property
    def createUserId(self):
        return self.__raw["attributes"].get("createUserId", None)
    @property
    def createUserName(self):
        return self.__raw["attributes"].get("createUserName", None)
    @property
    def lastModifiedTime(self):
        return self.__raw["attributes"].get("lastModifiedTime", None)
    @property
    def lastModifiedUserId(self):
        return self.__raw["attributes"].get("lastModifiedUserId", None)
    @property
    def lastModifiedUserName(self):
        return self.__raw["attributes"].get("lastModifiedUserName", None)
    @property
    def versionNumber(self):
        return self.__raw["attributes"].get("versionNumber", None)
    @property
    def mimeType(self):
        return self.__raw["attributes"].get("mimeType", None)
    @property
    def parentProjectId(self):
        return self.__parentProjectId

    @classmethod
    def version_by_id(cls, token, projectId, versionId):
        '''Returns the version with the given version_id<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{pId}/versions/{verId}".format(pId=projectId, verId=versionId)
        r = requests.get(endpointUrl, headers=token.XUser).json()
        checkResponse(r)
        return cls(r, projectId)

# TODO LEFT
# Projects
# GET projects/:project_id/downloads/:download_id
# GET projects/:project_id/jobs/:job_id
# POST projects/:project_id/downloads
# POST projects/:project_id/storage

# Folders
# GET projects/:project_id/folders/:folder_id/parent
# GET projects/:project_id/folders/:folder_id/refs
# GET projects/:project_id/folders/:folder_id/relationships/links
# GET projects/:project_id/folders/:folder_id/relationships/refs
# GET projects/:project_id/folders/:folder_id/search
# POST projects/:project_id/folders
# POST projects/:project_id/folders/:folder_id/relationships/refs
# PATCH projects/:project_id/folders/:folder_id

# Items
# GET projects/:project_id/items/:item_id/parent
# GET projects/:project_id/items/:item_id/refs
# GET projects/:project_id/items/:item_id/relationships/links
# GET projects/:project_id/items/:item_id/relationships/refs
# POST projects/:project_id/items
# POST projects/:project_id/items/:item_id/relationships/refs
# PATCH projects/:project_id/items/:item_id

# Versions
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