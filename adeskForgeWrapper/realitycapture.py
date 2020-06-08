# ----------
# Wrapper for REALITY CAPTURE API
# https://forge.autodesk.com/en/docs/reality-capture/v1/reference/http/
# ----------
'''Module for the Reality Capture API'''
from .utils import checkScopes
from .utils import checkResponse
from .utils import RECAP_API
from .utils import batch
from . import client
from . import AFWExceptions
import json

from requests_toolbelt import MultipartEncoder
from webbrowser import open as web_open
import requests

class Options(object):
    '''Class used to organize request options for this module'''
    @staticmethod
    def create_scene_options(scenename, Format, scenetype, **kwargs):
        '''Options for Photoscene.create_scene<br>
        scenename - Your scene name<br>
        format - Supported values are rcm, rcs, obj, fbx, ortho, report. Output file format; multiple file formats can be listed in a comma-delimited list.<br>
        scenetype - Supoprted values are aerial, object. Specifies the subject type of the photoscene.<br><br>

        kwargs:<br>
        callback<br>
        gpstype<br>
        hubprojectid<br>
        hubfolderid<br>
        version<br>
        metadata<br>
        '''

        callback = kwargs.get("callback", None)
        gpstype = kwargs.get("gpstype", None)
        metadata = kwargs.get("metadata", None)
        
        if callback is not None:
            if "http://" not in callback or "https://" not in callback:
                callback = "email://{}".format(callback)

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
                "hubprojectid" : kwargs.get("hubprojectid", None),
                "hubfolderid" : kwargs.get("hubfolderid", None),
                "version" : kwargs.get("version", None),
                "metadata" : kwargs.get("metadata", None)
                }

        data = {k : v for k,v in data.items() if v is not None} 
        return data # Works as dict type. Returns an error using json.dumps, why...


class Photoscene(object):
    '''A “photoscene” entity provides a common representation of a photo-to-3D project. <br>
    Certain fields will only be available after processing is complete.'''
    def __init__(self, rawDict):
        self._raw = rawDict

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw["Photoscene"].get("photosceneid", None)
    @property
    def progressmsg(self):
        return self._raw.get("progressmsg", None)
    @property
    def progress(self):
        return self._raw.get("progress", None)
    @property
    def scenelink(self):
        return self._raw.get("scenelink", None)
    @property
    def filesize(self):
        return self._raw.get("filesize", None)
    @property
    def resultmsg(self):
        return self._raw.get("resultmsg", None)

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
        endpoint_url = RECAP_API+"/photoscene"
        r = requests.post(endpoint_url, headers=token.url_encoded, data=create_scene_options).json()
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

            endpoint_url = RECAP_API+"/file"
            r = requests.post(endpoint_url, headers=headers, data=payload).json()
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
        endpoint_url = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.post(endpoint_url, headers=token.url_encoded).json()
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
        endpoint_url = RECAP_API+"/photoscene/{phId}/progress".format(phId = self.id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
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
        endpoint_url = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.delete(endpoint_url,headers=token.url_encoded).json()
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
        endpoint_url = RECAP_API+"/photoscene/{phId}".format(phId = Id)
        r = requests.delete(endpoint_url,headers=token.url_encoded).json()
        if "Error" in r:
            checkResponse(r["Error"])
        elif r["msg"] == "No error":
            print("Photoscene successfully deleted")
            return True

    def get_download_url(self, token: client.Token, Format, autoraise=False):
        '''Returns a time-limited HTTPS link to an output file of the specified format.<br>
        Scope - data:read<br><br>
        Note: The link will expire 30 days after the date of processing completion.'''
        checkScopes(token, "data:read")
        params = {"format":Format}
        endpoint_url = RECAP_API+"/photoscene/{phId}".format(phId = self.id)
        r = requests.get(endpoint_url,headers=token.get_header, params=params).json()
        if autoraise:
            web_open(r["Photoscene"]["scenelink"], new = 0, autoraise=autoraise)
        print(r["Photoscene"]["scenelink"])

    def cancel_progress(self, token: client.Token):
        '''Aborts the processing of a photoscene and marks it as cancelled.<br>
        Scope - data:write<br>
        
        Returns True if cancel was successful'''
        checkScopes(token, "data:write")
        endpoint_url = RECAP_API+"/photoscene/{phId}/cancel".format(phId = self.id)
        r = requests.post(endpoint_url, headers=token.url_encoded).json()
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