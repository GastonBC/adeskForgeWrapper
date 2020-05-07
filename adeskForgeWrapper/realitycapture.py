'''Module for the Reality Capture API'''
from .utils import checkScopes
from .utils import checkResponse
from .utils import RECAP_API
from .utils import batch
from . import client
from . import AFWExceptions
import json

from requests_toolbelt import MultipartEncoder
import requests

class Options(object):
    '''Class used to organize request options for this module'''
    @staticmethod
    def create_scene_options(scenename, Format = "rcm", scenetype = "aerial", callback = None, gpstype = None, hubprojectid = None,
                hubfolderid = None, version = "2.0", metadata = None):
        '''Options for Photoscene.create'''

        if scenetype != "aerial":
            if Format == "rcs" or Format == "ortho" or Format == "report":
                raise AFWExceptions.AFWError("That format parameter is only available if scenetype is set to aerial")

            elif gpstype != None:
                pass #TODO Check 

            elif metadata != None:
                raise AFWExceptions.AFWError("Metadata fine tuning parameters are available only if scenetype is set to aerial")
        data = {
                "scenename" : scenename,
                "callback" : callback,
                "format": Format,
                "scenetype" : scenetype,
                "gpstype" : gpstype,
                "hubprojectid" : hubprojectid,
                "hubfolderid" : hubfolderid,
                "version" : version,
                "metadata" : metadata
                }
        if callback is not None:
            if "http://" in callback or "https://" in callback:
                data["callback"] = callback
            else:
                data["callback"] = "email://{}".format(callback)
        data = {k : v for k,v in data.items() if v is not None} 
        return data # Works as dict type. Returns an error using json.dumps, why...


class Photoscene(object):
    '''A “photoscene” entity provides a common representation of a photo-to-3D project. <br>
    Certain fields will only be available after processing is complete.'''
    def __init__(self, rawDict):
        self.__raw = rawDict

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__raw.get("photosceneid", None)
    @property
    def progressmsg(self):
        return self.__raw.get("progressmsg", None)
    @property
    def progress(self):
        return self.__raw.get("progress", None)
    @property
    def scenelink(self):
        return self.__raw.get("scenelink", None)
    @property
    def filesize(self):
        return self.__raw.get("filesize", None)
    @property
    def resultmsg(self):
        return self.__raw.get("resultmsg", None)

    @classmethod
    def photoscene_by_id(cls, PhotosceneId):
        rawDict = {
        "Photoscene": {
        "photosceneid": PhotosceneId
         }
        }
        return cls(rawDict)
    
    @classmethod
    def create_scene(cls, token: client.Token, create_scene_options):
        '''Creates and initializes a photoscene for reconstruction.<br>
        Scope - data:write
        psOptions - Options.PhotosceneCreationOptions'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene"
        r = requests.post(endpointUrl, headers=token.urlEncoded, data=create_scene_options).json()
        checkResponse(r)
        print("Photoscene ID:", '{}'.format(r['Photoscene'].get("photosceneid")))
        return cls(r)
    
    def upload_files(self, token: client.Token, files: list, batchSize=3):
        '''Adds one or more files to a photoscene.<br>
        Scope - data:write<br>
        files - A list containing the path to the images you want to upload<br>
        batchSize - Number of files per request must be limited to avoid timeouts<br>
        Recommended batch size 3 (default)<br><br>

        Files can be added to photoscene either by uploading them directly or by providing public HTTP/HTTPS links.
        Although uploading multiple files at the same time might be more efficient, you should limit the number 
        of files per request depending on your available bandwidth to avoid timeouts.<br>
        Note: Uploaded files will be deleted after 30 days.'''
        checkScopes(token, "data:write")
        filesUploaded=[]

        for x in batch(files, batchSize):
            n=-1
            fields = {'photosceneid':self.id, 'type': 'image'}
            for a in x:
                n=n+1
                a = a.replace("/", "\\")
                fields["file[{x}]".format(x=n)] = (a, open(a,'rb'), 'image/jpg')

            payload = MultipartEncoder(fields)
            headers = {'Content-Type': payload.content_type, 'Authorization': 'Bearer {}'.format(token.access_token)}

            endpointUrl = RECAP_API+"/file"
            r = requests.post(endpointUrl, headers=headers, data=payload).json()
            if "Error" in r:
                checkResponse(r["Error"])
            else:
                print(len(x), "uploaded")
                for raw in r["Files"]["file"]:
                    filesUploaded.append(File(raw, self.id))
        print("Success")
        return filesUploaded
        

    def start_processing(self, token: client.Token):
        '''Starts photoscene processing.<br>
        Scope - data:write<br>

        The main processing steps involve: camera calibration, mesh reconstruction, texturing, and any necessary output file format conversions, in that order.<br>
        This method should not be called until a photoscene has been created and at least three images have been added to the photoscene.<br>
        Note: Progress of the processing can be monitored with the getProgress(token)<br>
        Returns True if request was successful'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.post(endpointUrl, headers=token.urlEncoded).json()
        checkResponse(r)
        if "Error" in r:
            checkResponse(r["Error"])
        else:
            print("Processing started")
            return True

    def get_progress(self, token: client.Token):
        '''Returns the processing progress and status of a photoscene.<br>
        Scope - data:read'''
        checkScopes(token, "data:read")
        endpointUrl = RECAP_API+"/photoscene/{phId}/progress".format(phId = self.id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        if "Error" in r:
            checkResponse(r["Error"])
        else:
            print("{}%".format(r["Photoscene"]["progress"]))
            print(r["Photoscene"]["progressmsg"])

    def delete_scene(self, token: client.Token):
        '''Deletes a photoscene and its associated assets (images, output files, ...).<br>
        Scope - data:write<br><br>
        
        Returns True if deletion was successful'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.delete(endpointUrl,headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            print("Photoscene successfully deleted")

    @staticmethod
    def delete_scene_by_id(token: client.Token, Id: str):
        '''Deletes a photoscene and its associated assets (images, output files, ...) by ID<br>
        Scope - data:write<br><br>
        
        Returns True if deletion was successful'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = Id)
        r = requests.delete(endpointUrl,headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            print("Photoscene successfully deleted")
            return True

    def get_download_url(self, token: client.Token, Format):
        '''Returns a time-limited HTTPS link to an output file of the specified format.<br>
        Scope - data:read<br><br>
        Note: The link will expire 30 days after the date of processing completion.'''
        checkScopes(token, "data:read")
        params = {"format":Format}
        endpointUrl = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.get(endpointUrl,headers=token.getHeader, params=params).json()
        print(r) # TODO Review attributes usability

    def cancel_progress(self, token: client.Token):
        '''Aborts the processing of a photoscene and marks it as cancelled.<br>
        Scope - data:write<br>
        
        Returns True if cancel was successful'''
        checkScopes(token, "data:write")
        endpointUrl = RECAP_API+"/photoscene/{phId}/cancel".format(phId = self.id)
        r = requests.post(endpointUrl, headers=token.urlEncoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            print("Cancel successful")
            return True


class File(object):
    '''Class for the files returned by uploadFiles()'''
    def __init__(self, rawDict, psId):
        self.Id = rawDict.get("fileid")
        self.Name = rawDict.get("filename")
        self.Size = rawDict.get("filesize")
        self.PhotosceneId = psId

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

__pdoc__['File.Id'] = False
__pdoc__['File.Name'] = False
__pdoc__['File.Size'] = False
__pdoc__['File.PhotosceneId'] = False