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
        self.__type = rawDict.get("type", None)
        self.__hubId = rawDict.get("id", None)
        self.__name = rawDict["attributes"].get("name", None)
        self.__region = rawDict["attributes"].get("region", None)

    @property
    def apiType(self):
        return self.__apiType
    @property
    def raw(self):
        return self.__raw
    @property
    def type(self):
        return self.__type
    @property
    def hubId(self):
        return self.__hubId
    @property
    def name(self):
        return self.__name
    @property
    def region(self):
        return self.__region

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
    def getHubs(cls, token):
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

    def getProjectsByHub(self, token):
        '''Returns a list of all projects in the hub<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects".format(hId=self.hubId)
        projects = requests.get(endpointUrl,headers=token.getHeader).json()
        checkResponse(projects)
        return [Project(p) for p in projects["data"]]

    def projectById(self, token, projectId):
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
        self.__name = rawDict["attributes"].get("name", None)
        self.__id = rawDict.get("id", None)
        self.__hubId = rawDict["relationships"]["hub"]["data"].get("id", None)

    @property
    def id(self):
        return self.__id
    @property
    def raw(self):
        return self.__raw
    @property
    def apiType(self):
        return self.__apiType
    @property
    def name(self):
        return self.__name
    @property
    def hubId(self):
        return self.__hubId

    @classmethod
    def projectById(cls, token, hubId , pId):
        '''Returns a specific project by id
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}".format(hId=hubId, pId=pId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r["data"])

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
        endpointUrl = BASE_URL+"/project/v1/hubs/{hId}/projects/{pId}/topFolders".format(hId=self.hubId, pId=self.id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [Folder(tF) for tF in r["data"]]

class Folder(object):
    __apiType = "folders"
    def __init__(self, rawDict):
        '''Base folder class'''
        self.__raw = rawDict
        self.__id = rawDict.get("id", None)
        self.__name = rawDict["attributes"].get("name", None)
        self.__displayName = rawDict["attributes"].get("displayName", None)
        self.__createTime = rawDict["attributes"].get("createTime", None)
        self.__createUserId = rawDict["attributes"].get("createUserId", None)
        self.__createUserName = rawDict["attributes"].get("createUserName", None)
        self.__lastModifiedTime = rawDict["attributes"].get("lastModifiedTime", None)        
        self.__lastModifiedUserId = rawDict["attributes"].get("lastModifiedUserId", None)    
        self.__lastModifiedUserName = rawDict["attributes"].get("lastModifiedUserName", None)
        self.__objectCount = rawDict["attributes"].get("objectCount", None)
        self.__hidden = rawDict["attributes"].get("hidden", None)
    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    @property
    def displayName(self):
        return self.__displayName
    @property
    def createTime(self):
        return self.__createTime
    @property
    def createUserId(self):
        return self.__createUserId
    @property
    def createUserName(self):
        return self.__createUserName
    @property
    def lastModifiedTime(self):
        return self.__lastModifiedTime
    @property
    def lastModifiedUserId(self):
        return self.__lastModifiedUserId
    @property
    def lastModifiedUserName(self):
        return self.__lastModifiedUserName
    @property
    def objectCount(self):
        return self.__objectCount
    @property
    def hidden(self):
        return self.__hidden

    @classmethod
    def folderById(cls, token: Token, projectId, folderId):
        '''Returns a specific folder by id
        Scope data:read
        projectId: the project id in which the folder is contained
        folderId: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=projectId, f_id=folderId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r["data"])

    @classmethod
    def createFolder(cls, token: Token, project: Project, folderId):
        '''Returns a specific folder by id
        Scope data:read
        p_id: the project id in which the folder is contained
        f_id: the folder id'''
        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/data/v1/projects/{p_id}/folders/{f_id}".format(p_id=project.Id, f_id=folderId)
        r = requests.get(endpointUrl ,headers=token.getHeader).json()
        checkResponse(r)
        return cls(r["data"])

    def getContents(self, token, projectId):
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
                results.append(Folder(res))
            elif res["type"] == "items":
                results.append(Item(res))
            elif res["type"] == "versions":
                pass
        return results

class Item(object):
    def __init__(self, rawDict):
        self.__raw = rawDict
        self.__id = rawDict.get("id", None)
        self.__displayName = rawDict["attributes"].get("displayName", None)
        self.__createTime = rawDict["attributes"].get("createTime", None)
        self.__createUserId = rawDict["attributes"].get("createUserId", None)
        self.__createUserName = rawDict["attributes"].get("createUserName", None)
        self.__lastModifiedTime = rawDict["attributes"].get("lastModifiedTime", None)
        self.__lastModifiedUserId = rawDict["attributes"].get("lastModifiedUserId", None)
        self.__lastModifiedUserName = rawDict["attributes"].get("lastModifiedUserName", None)
        self.__hidden = rawDict["attributes"].get("hidden", None)
        self.__reserved = rawDict["attributes"].get("reserved", None)
        self.__extension = rawDict["attributes"].get("extension", None)
    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def displayName(self):
        return self.__displayName
    @property
    def createTime(self):
        return self.__createTime
    @property
    def createUserId(self):
        return self.__createUserId
    @property
    def createUserName(self):
        return self.__createUserName
    @property
    def lastModifiedTime(self):
        return self.__lastModifiedTime
    @property
    def lastModifiedUserId(self):
        return self.__lastModifiedUserId
    @property
    def lastModifiedUserName(self):
        return self.__lastModifiedUserName
    @property
    def hidden(self):
        return self.__hidden
    @property
    def reserved(self):
        return self.__reserved
    @property
    def extension(self):
        return self.__extension

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