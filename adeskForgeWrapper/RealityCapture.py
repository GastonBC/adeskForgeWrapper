from .client import checkScopes
from .client import checkResponse
from .urls import RECAP_API
from . import client
from . import fpwExceptions
import os

import requests

class PhotosceneCreationOptions(object):
    '''Class used to organize request options for this module'''
    def __init__(self, scenename: str, callback = None, Format = "rcm", scenetype = "aerial", gpstype = None, hubprojectid = None,
                hubfolderid = None, version = "2.0", metadata = None):
        if scenetype != "aerial":
            if Format == "rcs" or Format== "ortho" or Format == "report":
                raise fpwExceptions.forgeException("That format parameter is only available if scenetype is set to aerial")

            elif gpstype != None:
                pass #TODO Check 

            elif metadata != None:
                raise fpwExceptions.forgeException("Metadata fine tuning parameters are available only if scenetype is set to aerial")

        if "http://" in callback or "https://" in callback:
            self.callback = callback
        else:
            self.callback = "email://{}".format(callback)
        self.scenename = scenename
        self.Format = Format
        self.scenetype = scenetype
        self.gpstype = gpstype
        self.hubprojectid = hubprojectid
        self.hubfolderid = hubfolderid
        self.version = version
        self.metadata = metadata

    @classmethod
    def defaultObjectScene(cls):
        return cls(scenename="afwDefaultObject", scenetype="object")



class Photoscene(object):
    '''A “photoscene” entity provides a common representation of a photo-to-3D project. <br>
    Certain fields will only be available after processing is complete.
    Photoscene.raw<br>
    Photoscene.scenename<br>
    Photoscene.callback<br>
    Photoscene.format<br>
    Photoscene.scenetype<br>
    Photoscene.gpstype<br>
    Photoscene.hubprojectid<br>
    Photoscene.hubfolderid<br>
    Photoscene.version<br>
    Photoscene.metadata<br>'''
    def __init__(self, rawDict, Id):
        self.__raw = rawDict
        self.__scenename = rawDict.get("scenename") or None
        self.__callback = rawDict.get("callback") or None
        self.__format = rawDict.get("format") or None
        self.__scenetype = rawDict.get("scenetype") or None
        self.__gpstype = rawDict.get("gpstype") or None
        self.__hubprojectid = rawDict.get("hubprojectid") or None
        self.__hubfolderid = rawDict.get("hubfolderid") or None
        self.__version = rawDict.get("version") or None
        self.__metadata = rawDict.get("metadata") or None
        self.__Id = rawDict.get("photosceneid") or Id
    
    @property
    def raw(self):
        return self.__raw
    @property
    def Id(self):
        return self.__Id
    @property
    def scenename(self):
        return self.__scenename
    @property
    def callback(self):
        return self.__callback
    @property
    def format(self):
        return self.__format
    @property
    def scenetype(self):
        return self.__scenetype
    @property
    def gpstype(self):
        return self.__gpstype
    @property
    def hubprojectid(self):
        return self.__hubprojectid
    @property
    def hubfolderid(self):
        return self.__hubfolderid
    @property
    def version(self):
        return self.__version
    @property
    def metadata(self):
        return self.__metadata

    @classmethod
    def psById(cls, PhotosceneId):
        rawDict = {
        "Photoscene": {
        "photosceneid": PhotosceneId
                      }
         }
        return cls(rawDict, PhotosceneId)
    
    @classmethod
    def create(cls, token: client.Token, psOptions: PhotosceneCreationOptions):
        '''Creates and initializes a photoscene for reconstruction.<br>
        Scope data:write'''
        checkScopes(token, "data:write")
        data = {
        "scenename" : psOptions.scenename,
        "callback" : psOptions.callback,
        "format": psOptions.Format,
        "scenetype" : psOptions.scenetype,
        "gpstype" : psOptions.gpstype,
        "hubprojectid" : psOptions.hubprojectid,
        "hubfolderid" : psOptions.hubfolderid,
        "version" : psOptions.version,
        "metadata" : psOptions.metadata
        }
        data = {k : v for k,v in data.items() if v is not None}
        endpointUrl = RECAP_API+"/photoscene"
        r = requests.post(endpointUrl, headers=token.urlEncoded, data=data).json()
        checkResponse(r)
        print("Photoscene ID:", r.get("photosceneid"))
        return cls(r, data)
    
    def uploadFiles(self, token: client.Token):
        '''Adds one or more files to a photoscene.<br>
        Scope data:write<br><br>
        Files can be added to photoscene either by uploading them directly or by providing public HTTP/HTTPS links.
        Although uploading multiple files at the same time might be more efficient, you should limit the number 
        of files per request depending on your available bandwidth to avoid timeouts.<br>
        Note: Uploaded files will be deleted after 30 days.'''
        checkScopes(token, "data:write")
        import tkinter as tk
        from tkinter import filedialog
        application_window = tk.Tk()
        application_window.withdraw()
        answer = filedialog.askopenfilenames(parent=application_window,
                                            initialdir=os.getcwd(),
                                            title="Please select one or more files:",
                                            filetypes=[("Image files", ".jpg .jpeg")])
        if answer != "":
            payload = {'photosceneid':self.Id, 'type': 'image'}
            files = []
            n=-1
            for a in answer:
                n = n+1
                a = a.replace("/", "\\")
                files.append(("file[{x}]".format(x=n), open(a,"rb")))

                # files["file[{x}]".format(x=n)] = (a, open(a,"rb"))
            endpointUrl = RECAP_API+"/file"
            r = requests.post(endpointUrl, headers=token.formData, data=payload, files=files).json()
            if "Error" in r:
                checkResponse(r["Error"])
            else:
                print(r)

    def startProcessing(self, token: client.Token):
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.Id)
        r = requests.post(endpointUrl, headers=token.urlEncoded).json()
        checkResponse(r)
        if "Error" in r:
            checkResponse(r["Error"])
        else:
            print(r)

    def getProgress(self, token: client.Token):
        '''Returns the processing progress and status of a photoscene.'''
        checkScopes(token, "data:read")
        endpointUrl = RECAP_API+"/photoscene/{phId}/progress".format(phId = self.Id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        if "Error" in r:
            checkResponse(r["Error"])
        else:
            print("{}%".format(r["Photoscene"]["progress"]))
            print(r["Photoscene"]["progressmsg"])

    def deleteScene(self, token: client.Token):
        '''Deletes a photoscene and its associated assets (images, output files, ...).'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.Id)
        r = requests.delete(endpointUrl,headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            print("Photoscene successfully deleted")

    @classmethod
    def deleteSceneById(self, token: client.Token, Id: str):
        '''Deletes a photoscene and its associated assets (images, output files, ...).'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = Id)
        r = requests.delete(endpointUrl,headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            return True

    def getDownloadURL(self, token: client.Token, Format = None):
        '''Returns a time-limited HTTPS link to an output file of the specified format.<br>
        Note: The link will expire 30 days after the date of processing completion.'''
        checkScopes(token, "data:read")
        if Format is None:
            params = ("format", self.format)
            endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.Id)
            r = requests.get(endpointUrl,headers=token.getHeader, params=params).json()
        elif Format is not None:
            params = ("format", Format)
            endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.Id)
            r = requests.get(endpointUrl, headers=token.getHeader, params=params).json()
        print(r) # TODO Review attributes usability

    def cancelProgress(self, token: client.Token):
        '''Aborts the processing of a photoscene and marks it as cancelled.'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}/cancel".format(phId = self.Id)
        r = requests.post(endpointUrl, headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            return True


__pdoc__ = {}

__pdoc__['Photoscene.raw'] = False      
__pdoc__['Photoscene.scenename'] = False
__pdoc__['Photoscene.callback'] = False 
__pdoc__['Photoscene.format'] = False   
__pdoc__['Photoscene.scenetype'] = False
__pdoc__['Photoscene.gpstype'] = False
__pdoc__['Photoscene.hubprojectid'] = False
__pdoc__['Photoscene.hubfolderid'] = False
__pdoc__['Photoscene.version'] = False
__pdoc__['Photoscene.metadata'] = False