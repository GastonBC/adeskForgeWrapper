# ----------
# Wrapper for BIM360 API
# https://forge.autodesk.com/en/docs/bim360/v1/reference/http/
# ----------

import requests

from . import AFWExceptions
from . import client
from .utils import checkScopes
from .utils import checkResponse
from .utils import AUTODESK_BASE_URL as BASE_URL
import json


class Options(object):
    '''Some methods require data and parameters in diferent formats, 
    this class makes it easy to add those and ensures the information is sent the right way.'''
    @staticmethod
    def createProjectOptions(name, start_date, end_date, project_type, value, currency, service_types=None,
                            job_number=None, address_line_1=None, address_line_2=None, city=None, state_or_province=None, 
                            postal_code=None, country=None, business_unit_id=None, timezone=None, language=None, construction_type=None, 
                            contract_type=None, template_project_id=None, include_companies=None, include_locations=None):
        '''Data used to create a project.<br>
        Note that NAME, START_DATE, END_DATE, PROJECT_TYPE, VALUE and CURRENCY are required values.
        start_date - YYYY-MM-DD
        end_date - YYYY-MM-DD, later than start date
        project_type - Refer to parameters (https://forge.autodesk.com/en/docs/bim360/v1/overview/parameters/)
        currency - Refer to parameters
        language - Refer to parameters'''

        data = {
            "name":name,
            "service_types":service_types,
            "start_date":start_date,
            "end_date":end_date,
            "project_type":project_type, 
            "value":value,
            "currency":currency,
            "job_number":job_number,
            "address_line_1":address_line_1,
            "address_line_2":address_line_2,
            "city":city,
            "state_or_province":state_or_province,
            "postal_code":postal_code,
            "country":country,
            "business_unit_id":business_unit_id,
            "timezone":timezone,
            "language":language,
            "construction_type":construction_type,
            "contract_type":contract_type,
            "template_project_id":template_project_id,
            "include_companies":include_companies,
            "include_locations":include_locations,
        }
        data = {k : v for k,v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def updateProjectOptions(name = None, service_types = None, status = None, start_date = None,
                             end_date = None, project_type = None, value = None, currency = None, job_number = None,
                             address_line_1 = None, address_line_2 = None, city = None, state_or_province = None,
                             postal_code = None, country = None, business_unit_id = None, timezone = None, language = None,
                             construction_type = None, contract_type = None):
        '''Options to update a project.'''
        
        data = {
            "name":name,
            "service_types":service_types,
            "status":status,
            "start_date":start_date,
            "end_date":end_date,
            "project_type":project_type,
            "value":value,
            "currency":currency,
            "job_number":job_number,
            "address_line_1":address_line_1,
            "address_line_2":address_line_2,
            "city":city,
            "state_or_province":state_or_province,
            "postal_code":postal_code,
            "country":country,
            "business_unit_id":business_unit_id,
            "timezone":timezone,
            "language":language,
            "construction_type":construction_type,
            "contract_type":contract_type
        }
        data = {k : v for k,v in data.items() if v is not None} 
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def exportPDFOptions(versionId: str, includeMarkups: bool = False, includeHyperlinks: bool = False):
        '''Options to export PDFs'''
        if type(includeMarkups) != bool or type(includeMarkups) != bool:
            raise TypeError("includeMarkups/includeHyperlinks expected bool")
        data={"includeMarkups": includeMarkups,
              "includeHyperlinks": includeHyperlinks}
        return (versionId, data)

    @staticmethod
    def updateProjectUserOptions(status, company_id):
        '''Options to update a user'''
        data = {
                "status": status,
                "company_id": company_id
                }
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def updateCompanyOptions(name = None, trade = None, address_line_1 = None, address_line_2 = None, city = None, state_or_province = None, country = None,
                             phone = None, website_url = None, description = None, erp_id = None, tax_id = None):
        '''Options for updateCompany'''
        
        data = {"name":name,
                "trade":trade,
                "address_line_1":address_line_1,
                "address_line_2":address_line_2,
                "city":city,
                "state_or_province":state_or_province,
                "country":country,
                "phone":phone,
                "website_url":website_url,
                "description":description,
                "erp_id":erp_id,
                "tax_id":tax_id
                }
        data = {k : v for k,v in data.items() if v is not None} 
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def searchCompaniesOptions(name = None, trade = None, operator = None, partial = None, limit = None, offset = None, sort = None, field = None):
        '''Options for searchCompany'''
        params = (
                ('name', name),
                ('trade', trade),
                ('operator', operator),
                ('partial', partial),
                ('limit', limit),
                ('offset', offset),
                ('sort', sort),
                ('field', field)
        )
        return params

    @staticmethod
    def addUserToProjectOptions(email = None, user_id = None, services = None, docManagementAccessLevel = None,
                                projectAdminAccessLevel = None, company_id = None, industry_roles = None):
        '''Use this method for each user you want to update'''
        data={
            "email": email,
            "user_id": user_id,
            "services": {
                        "document_management": {"access_level": docManagementAccessLevel},
                        "project_administration": {"access_level": projectAdminAccessLevel},
                        },
            "company_id":company_id,
            "industry_roles":industry_roles
          }
        return data

class Project(object):
    '''Class for B360 API projects. Properties below
    Project.raw<br>
    Project.id<br>
    Project.accId<br>
    Project.name<br>
    Project.start_date<br>
    Project.end_date<br>
    Project.project_type<br>
    Project.value<br>
    Project.currency<br>
    Project.status<br>
    Project.job_number<br>
    Project.address_line_1<br> 
    Project.address_line_2<br>
    Project.city<br>
    Project.state_or_province<br>
    Project.postal_code<br>
    Project.country<br>
    Project.business_unit_id<br>
    Project.timezone<br>
    Project.language <br>
    Project.construction_type<br>
    Project.contract_type<br>
    Project.service_types<br>
    Project.created_at<br>
    Project.updated_at'''
#hiddenRegion
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__id = rawDict.get("id") or None
        self.__accId = rawDict.get("account_id") or None
        self.__status = rawDict.get("status") or None
        self.__name = rawDict.get("name") or None
        self.__service_types = rawDict.get("service_types") or None
        self.__start_date = rawDict.get("start_date") or None
        self.__end_date = rawDict.get("end_date") or None
        self.__project_type = rawDict.get("project_type") or None
        self.__value = rawDict.get("value") or None
        self.__currency = rawDict.get("currency") or None
        self.__job_number = rawDict.get("job_number") or None
        self.__address_line_1 = rawDict.get("address_line_1") or None
        self.__address_line_2 = rawDict.get("address_line_2") or None
        self.__city = rawDict.get("city") or None
        self.__state_or_province = rawDict.get("state_or_province") or None
        self.__postal_code = rawDict.get("postal_code") or None
        self.__country = rawDict.get("country") or None
        self.__business_unit_id = rawDict.get("business_unit_id") or None
        self.__timezone = rawDict.get("timezone") or None
        self.__language = rawDict.get("language") or None
        self.__construction_type = rawDict.get("construction_type") or None
        self.__contract_type = rawDict.get("contract_type") or None
        self.__template_project_id = rawDict.get("template_project_id") or None
        self.__include_companies = rawDict.get("include_companies") or None
        self.__include_locations = rawDict.get("include_locations") or None
        self.__created_at = rawDict.get("created_at") or None
        self.__updated_at = rawDict.get("updated_at") or None
    @property
    def raw(self):
        '''The raw dictionary response'''
        return self.__raw
    @property
    def name(self):
        '''Name of the project'''
        return self.__name
    @property
    def id(self):
        '''Project ID'''
        return self.__id
    @property
    def accId(self):
        '''Account ID'''
        return self.__accId
    @property
    def status(self):
        '''
        The status of project.

        Possible values:
        active: project is active with at least one project admin added
        pending: project has been created but pending becuase no project admin added
        inactive: project is suspended
        archived: project is archived and displayed only in the archived list'''
        return self.__status
    @property
    def service_types(self):
        return self.__service_types
    @property
    def start_date(self):
        return self.__start_date
    @property
    def end_date(self):
        return self.__end_date
    @property
    def project_type(self):
        '''
        The type of project; accepts preconfigured and customized project types

        Max length: 255

        Refer to the preconfigured project_type list in
        the Parameters guide.'''
        return self.__project_type
    @property
    def value(self):
        '''Monetary value of the project'''
        return self.__value
    @property
    def currency(self):
        '''
        Currency for project value
        Refer to the currency list in the Parameters guide.'''
        return self.__currency
    @property
    def job_number(self):
        return self.__job_number
    @property
    def address_line_1(self):
        return self.__address_line_1
    @property
    def address_line_2(self):
        return self.__address_line_2
    @property
    def city(self):
        return self.__city
    @property
    def state_or_province(self):
        return self.__state_or_province
    @property
    def postal_code(self):
        return self.__postal_code
    @property
    def country(self):
        return self.__country
    @property
    def business_unit_id(self):
        return self.__business_unit_id
    @property
    def timezone(self):
        return self.__timezone
    @property
    def language(self):
        return self.__language
    @property
    def construction_type(self):
        return self.__construction_type
    @property
    def contract_type(self):
        return self.__contract_type
    @property
    def template_project_id(self):
        return self.__template_project_id
    @property
    def include_companies(self):
        return self.__include_companies
    @property
    def include_locations(self):
        return self.__include_locations
    @property
    def created_at(self):
        return self.__created_at
    @property
    def updated_at(self):
        return self.__updated_at
#endRegion

    @classmethod
    def getProjects(cls, token: client.Token):
        '''Query all the projects in a specific BIM 360 account.<br>
        Scope - account:read<br>
        Returns a list of project objects.'''
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/projects".format(aId=token.bimAccId)
        checkScopes(token, "account:read")
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(p) for p in r]


    @classmethod
    def getProjectById(cls, token: client.Token, p_id):
        '''Query the details of a specific BIM 360 project.<br>
        Scope: account:read'''
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/projects/{pId}".format(aId=token.bimAccId, pId=p_id)
        checkScopes(token, "account:read")
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r)


    @classmethod
    def createProject(cls, token: client.Token, creationOps):
        '''Create a new BIM 360 project in a specific BIM 360 account.<br>
        Scope - account:write<br>
        creationOps - From Options Class, createProjectOptions()'''
        checkScopes(token, "account:write")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/projects".format(aId=token.bimAccId)
        r = requests.post(endpointUrl, headers=token.patchHeader, data=creationOps).json()
        print(r)
        checkResponse(r)
        return cls(r)

    def updateProject(self, token: client.Token, updateProjectOptions):
        '''Update the properties of only the specified attributes of a specific BIM 360 project.<br>
           Scope - account:write account:read'''
        checkScopes(token, "account:read account:write")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/projects/{pId}".format(aId=self.accId, pId=self.id)
        r = requests.patch(endpointUrl, headers=token.patchHeader, data=updateProjectOptions).json()
        checkResponse(r)
        return Project(r)
    
    def getUsersFromProject(self, token: client.Token):
        '''Retrieves information about all the users in a project.<br>
        To get information about all the users in an account, see GET accounts/users.<br>
        Scope - account:read'''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/bim360/admin/v1/projects/{pId}/users".format(pId=self.id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [User(u) for u in r["results"]]

    def getUserFromProjectAndId(self, token: client.Token, userId):
        '''Retrieves detailed information about a single user in a project.<br>
        Scope - account:read'''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/bim360/admin/v1/projects/{pId}/users/{uId}".format(pId=self.id, uId=userId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return User(r)

    def addUsersToProject(self, token: client.Token, addUserToProjectOps: list):
        # TODO TO REVIEW. ITEMS FAIL
        # TODO ADD NEW HEADER ITEM, X-USER-ID TO TOKEN
        # TODO ADD OPTIONS class
        '''Adds users (project admin and project user) to a project. You can add up to 50 users per call.<br>
            Scope - account:write<br>
            addUserToProjectOps - MUST BE A LIST of Options.addUserToProjectOptions<br>

            To add users to an account (account user), see POST users.<br>
            You can specify the following details about the user:<br>
            The user’s access level for the project (admin or user).<br>
            The company the user is assigned to for the project.<br>
            The industry roles assigned to the user for the project.<br>
            The user’s email address.<br><br>
            '''
        if type(addUserToProjectOps) != list:
            raise AFWExceptions.AFWError("addUserToProjectOps must be a list of Options.addUserToProjectOptions")
        checkScopes(token, "account:write")
        addUserToProjectOps = json.dumps(addUserToProjectOps)
        endpointUrl = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/users/import".format(aId=self.accId ,pId=self.id)
        r = requests.post(endpointUrl, headers=token.contentXUser, data=addUserToProjectOps).json()
        checkResponse(r)
        print("Success:", r["success"])
        print("Failed:", r["failure"])
        return [User.getUserById(token, u["user_id"]) for u in r["success_items"]]

    def updateProjectUserById(self, token: client.Token, userId, updateProjectUserOptions):
        '''Updates a user’s profile for a project, including:<br><br>

        The company the user is assigned to for the project.<br>
        The industry roles assigned to the user for the project.<br><br>
        Scope - account:write
        
        Returns a User object'''
        # TODO: Thinking about changing user id with user object, updating the user object with the response

        checkScopes(token, "account:write")
        endpointUrl = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/users/{uId}".format(aId=self.accId ,pId=self.id, uId=userId)
        r = requests.patch(endpointUrl, headers=token.contentXUser, data=updateProjectUserOptions).json()
        checkResponse(r)
        return User(r)
    def getIndustryRoles(self, token: client.Token):
        '''Retrieves the industry roles for the project. For example, contractor and architect.<br>
        Scope - account:read'''

        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/industry_roles".format(aId=self.accId ,pId=self.id)
        r = requests.get(endpointUrl, headers=token.patchHeader).json()
        checkResponse(r)
        return [IndustryRoles(i) for i in r]

    def exportPDF(self, token: client.Token, exportOptions):
        '''Exports a single page from an uploaded PDF file into a new PDF file.<br>
            You can also export the page’s markups (annotations) and hyperlinks.<br>
            Scope - data:read<br>
            exportOptions - exportPDFOptions()<br>
            Note that you can only export a page from a PDF file that was uploaded to the Plans folder or 
            to a folder nested under the Plans folder (attributes.extension.data.actions: SPLIT). BIM 360 Document Management 
            splits these files into separate pages (sheets) when they are uploaded, and assigns a separate ID to each page.<br>
            You can identify exportable PDF files, by searching for files with the following combmination of properties:<br><br>

            attributes.extension.type: items:autodesk.bim360.Document (identifies all files that are split into separate pages)<br>
            attributes.extension.data.sourceFileName: <filename>.pdf (identifies all PDF files)<br>
            You can export PDF pages both from PDF files that were uploaded via the BIM 360 Document Management UI and from 
            PDF files that were uploaded via BIM 360 endpoints. For more details about uploading documents to BIM 360 via the 
            BIM 360 endpoints, see the File Upload tutorial.<br><br>

            Note that this endpoint is asynchronous and initiates a job that 
            runs in the background, rather than halting execution of your program.<br>
            The response returns an export ID that you can use to call getPDFExport() 
            to verify the status of the job. When the job is complete, you can retrieve the data you need to download the exported page.<br><br>

            Note that the user must have permission to view files. For information about permissions, see the Help documentation.<br><br>

            For more details about exporting PDF files, see the PDF Export tutorial.<br><br>

            For more information about Document Management endpoints, see the Data Management API<br><br>
            '''

        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/bim360/docs/v1/projects/{pId}/versions/{vId}/exports".format(pId=self.id, vId=exportOptions[0])
        r = requests.post(endpointUrl, headers=token.patchHeader, data=str(exportOptions[1])).json()
        checkResponse(r)
        print("Id: {id}\nStatus: {status}".format(id=r["id"], status=r["status"]))
        return r

    def getPDFExport(self, token: client.Token, versionId: str, exportId: str):
        '''Returns the status of a PDF export job, as well as data you need to download the exported file when the export is complete.<br>
            The exportPDF() function initiates the job, and returns a job ID to be used in this endopint.<br>
            To download the exported PDF file after the job is complete, use GET :urn/manifest/:derivativeurn.<br><br>
            
            For more information about Document Management endpoints, see the Data Management API'''
            # TODO: Model derivative api function here

        checkScopes(token, "data:read")
        endpointUrl = BASE_URL+"/bim360/docs/v1/projects/{pId}/versions/{vId}/exports/{eId}".format(pId=self.id, vId=versionId, eId=exportId)
        r = requests.get(endpointUrl, headers=token.contentXUser).json()
        checkResponse(r)
        print(r) #TODO: Try, .json() may not work here. will probably find a way once model derivative api is running.
                 #TODO: Range header
        return r

class Company(object):
    '''Base class for B360 API companies. Properties below<br>
    Company.raw <br>
    Company.id<br>
    Company.accId<br>
    Company.name<br>
    Company.trade<br>
    Company.address_line_1<br>
    Company.address_line_2<br>
    Company.city<br>
    Company.postal_code<br>
    Company.state_or_province<br>
    Company.country<br>
    Company.phone<br>
    Company.website_url<br>
    Company.description<br>
    Company.created_at<br>
    Company.updated_at<br>
    Company.erp_id<br>
    Company.tax_id'''
#hiddenRegion
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__id = rawDict.get("id") or None
        self.__accId = rawDict.get("account_id") or None
        self.__name = rawDict.get("name") or None
        self.__trade = rawDict.get("trade") or None
        self.__address_line_1 = rawDict.get("address_line_1") or None
        self.__address_line_2 = rawDict.get("address_line_2") or None
        self.__city = rawDict.get("city") or None
        self.__postal_code = rawDict.get("postal_code") or None
        self.__state_or_province = rawDict.get("state_or_province") or None
        self.__country = rawDict.get("country") or None
        self.__phone = rawDict.get("phone") or None
        self.__website_url = rawDict.get("website_url") or None
        self.__description = rawDict.get("description") or None
        self.__created_at = rawDict.get("created_at") or None
        self.__updated_at = rawDict.get("updated_at") or None
        self.__erp_id = rawDict.get("erp_id") or None
        self.__tax_id = rawDict.get("tax_id") or None

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def accId(self):
        return self.__accId
    @property
    def name(self):
        return self.__name
    @property
    def trade(self):
        return self.__trade
    @property
    def address_line_1(self):
        return self.__address_line_1
    @property
    def address_line_2(self):
        return self.__address_line_2
    @property
    def city(self):
        return self.__city
    @property
    def postal_code(self):
        return self.__postal_code
    @property
    def state_or_province(self):
        return self.__state_or_province
    @property
    def country(self):
        return self.__country
    @property
    def phone(self):
        return self.__phone
    @property
    def website_url(self):
        return self.__website_url
    @property
    def description(self):
        return self.__description
    @property
    def created_at(self):
        return self.__created_at
    @property
    def updated_at(self):
        return self.__updated_at
    @property
    def erp_id(self):
        return self.__erp_id
    @property
    def tax_id(self):
        return self.__tax_id
#endRegion

    @classmethod
    def getCompanyById(cls, token: client.Token, c_id):
        '''Query the details of a specific partner company.<br>
        Scope: account:read'''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/companies/{cId}".format(aId=token.bimAccId, cId=c_id)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def getCompanies(cls, token: client.Token):
        '''Query all the partner companies in a specific BIM 360 account.<br>
        Scope account:read'''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/companies".format(aId=token.bimAccId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(c) for c in r]

    @classmethod
    def searchCompaniesByName(cls, token: client.Token, searchOps):
        '''Search partner companies in a specific BIM 360 account by name.<br>
        Scope - account:read<br>
        searchOps - Options.searchCompaniesOptions()
        '''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/companies/search".format(aId=token.bimAccId)
        r = requests.get(endpointUrl, headers=token.getHeader, params=searchOps).json()
        checkResponse(r)
        if r == []:
            return None
        else:
            return [cls(c) for c in r]

    @classmethod
    def importCompanies(cls, token: client.Token, Data: list):
        '''TODO: ---NOT WORKING??  TRY---
        Bulk import partner companies to the company directory in a specific BIM 360 account.
        (50 companies maximum can be included in each call.)
        Scope account:write
        
        Data template, must be a string.
        data = [{
                "name":"",
                "trade": "",
                "website_url": "",
                "city": "",
                "country": "",
                "address_line_1": "",
                "address_line_2": "",
                "postal_code": "",
                "erp_id":"",
                "tax_id":"",
                "phone": "",
                "description": ""
                }]'''
        checkScopes(token, "account:write")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/companies/import".format(aId=token.bimAccId)
        r = requests.post(endpointUrl, headers=token.patchHeader,data=Data).json()
        checkResponse(r)
        print("Success:", r["success"])
        print("Failure:", r["failure"])
        return [cls(c) for c in r["success_items"]]


    def updateCompany(self, token: client.Token, updateCompanyOptions):
        '''Update the properties of only the specified attributes of a specific partner company.<br>
        Scope - account:write'''
        checkScopes(token, "account:write")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/companies/{cId}".format(aId=self.accId, cId=self.id)
        r = requests.patch(endpointUrl, headers=token.patchHeader,data=updateCompanyOptions).json()
        checkResponse(r)
        return Company(r)

class User(object):
    '''User.raw<br>
    User.id<br>
    User.account_id<br>
    User.status<br>
    User.role<br>
    User.company_id<br>
    User.company_name<br>
    User.last_sign_in<br>
    User.email<br>
    User.name<br>
    User.nickname<br>
    User.first_name<br>
    User.last_name<br>
    User.uid<br>
    User.image_url<br>
    User.address_line_1<br>
    User.address_line_2<br>
    User.city<br>
    User.postal_code<br>
    User.state_or_province<br>
    User.country<br>
    User.phone<br>
    User.company<br>
    User.job_title<br>
    User.industry<br>
    User.about_me<br>
    User.created_at<br>
    User.updated_at<br>'''
#hiddenRegion
    def __init__(self, rawDict):
        self.__raw = rawDict
        self.__id = rawDict.get("id") or None
        self.__account_id = rawDict.get("account_id") or None
        self.__status = rawDict.get("status") or None
        self.__role = rawDict.get("role") or None
        self.__company_id = rawDict.get("company_id") or None
        self.__company_name = rawDict.get("company_name") or None
        self.__last_sign_in = rawDict.get("last_sign_in") or None
        self.__email = rawDict.get("email") or None
        self.__name = rawDict.get("name") or None
        self.__nickname = rawDict.get("nickname") or None
        self.__first_name = rawDict.get("first_name") or None
        self.__last_name = rawDict.get("last_name") or None
        self.__uid = rawDict.get("uid") or None
        self.__image_url = rawDict.get("image_url") or None
        self.__address_line_1 = rawDict.get("address_line_1") or None
        self.__address_line_2 = rawDict.get("address_line_2") or None
        self.__city = rawDict.get("city") or None
        self.__postal_code = rawDict.get("postal_code") or None
        self.__state_or_province = rawDict.get("state_or_province") or None
        self.__country = rawDict.get("country") or None
        self.__phone = rawDict.get("phone") or None
        self.__company = rawDict.get("company") or None
        self.__job_title = rawDict.get("job_title") or rawDict.get("jobTitle") or None
        self.__industry = rawDict.get("industry") or None
        self.__about_me = rawDict.get("about_me") or None
        self.__created_at = rawDict.get("created_at") or None
        self.__updated_at = rawDict.get("updated_at") or None

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def account_id(self):
        return self.__account_id
    @property
    def status(self):
        return self.__status
    @property
    def role(self):
        return self.__role
    @property
    def company_id(self):
        return self.__company_id
    @property
    def company_name(self):
        return self.__company_name
    @property
    def last_sign_in(self):
        return self.__last_sign_in
    @property
    def email(self):
        return self.__email
    @property
    def name(self):
        return self.__name
    @property
    def nickname(self):
        return self.__nickname
    @property
    def first_name(self):
        return self.__first_name
    @property
    def last_name(self):
        return self.__last_name
    @property
    def uid(self):
        return self.__uid
    @property
    def image_url(self):
        return self.__image_url
    @property
    def address_line_1(self):
        return self.__address_line_1
    @property
    def address_line_2(self):
        return self.__address_line_2
    @property
    def city(self):
        return self.__city
    @property
    def postal_code(self):
        return self.__postal_code
    @property
    def state_or_province(self):
        return self.__state_or_province
    @property
    def country(self):
        return self.__country
    @property
    def phone(self):
        return self.__phone
    @property
    def company(self):
        return self.__company
    @property
    def job_title(self):
        return self.__job_title
    @property
    def industry(self):
        return self.__industry
    @property
    def about_me(self):
        return self.__about_me
    @property
    def created_at(self):
        return self.__created_at
    @property
    def updated_at(self):
        return self.__updated_at
#endregion

    @classmethod
    def getUsersFromAccount(cls, token: client.Token):
        '''Query all the users in a specific BIM 360 account.<br>
        Scope account:read'''
        checkScopes(token, "account:read")
        endpointUrl = BASE_URL+"/hq/v1/accounts/{aId}/users".format(aId=token.bimAccId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(u) for u in r]

    @classmethod
    def getUserById(cls, token: client.Token, userId):
        '''Query the details of a specific user.<br>
        Scope account:read'''
        checkScopes(token, "account:read")
        endpointUrl = "/hq/v1/accounts/{aId}/users/{uId}".format(aId=token.bimAccId, uId=userId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def updateUserById(cls, token: client.Token, userId, updateUserOptions):
        '''Update a specific user’s status or default company. Data template below<br>
        Scope - account:write<br>
        updateUserOptions - From Options class'''
        checkScopes(token, "account:write")
        endpointUrl = "/hq/v1/accounts/{aId}/users/{uId}".format(aId=token.bimAccId, uId=userId)
        r = requests.patch(endpointUrl, headers=token.patchHeader, data=updateUserOptions).json()
        checkResponse(r)
        return cls(r)

    def updateUser(self, token: client.Token, updateUserOptions):
        '''Update a specific user’s status or default company. Data template below<br>
        Scope - account:write<br>
        updateUserOptions - From Options class'''
        checkScopes(token, "account:write")
        endpointUrl = "/hq/v1/accounts/{aId}/users/{uId}".format(aId=token.bimAccId, uId=self.id)
        r = requests.patch(endpointUrl, headers=token.patchHeader, data=str(updateUserOptions)).json()
        checkResponse(r)
        return User(r)

class IndustryRoles(object):
    '''IndustryRoles.raw<br>
    IndustryRoles.id<br>
    IndustryRoles.project_id<br>
    IndustryRoles.name<br>
    IndustryRoles.projectAdminAccess<br>
    IndustryRoles.insightAccess<br>
    IndustryRoles.docManagementAccess<br>
    IndustryRoles.member_group_id'''
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__id = rawDict.get("id") or None
        self.__name = rawDict.get("name") or None
        self.__project_id = rawDict.get("project_id") or None
        self.__projectAdminAccess = rawDict.get("services").get("project_administration").get("access_level") or None
        self.__insightAccess = rawDict.get("services").get("insight").get("access_level") or None
        self.__docManagementAccess = rawDict.get("services").get("document_management").get("access_level") or None
        self.__member_group_id = rawDict.get("member_group_id") or None

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
    def project_id(self):
        return self.__project_id
    @property
    def projectAdminAccess(self):
        return self.__projectAdminAccess
    @property
    def insightAccess(self):
        return self.__insightAccess
    @property
    def docManagementAccess(self):
        return self.__docManagementAccess
    @property
    def member_group_id(self):
        return self.__member_group_id

class BusinessUnits(object):
    '''BusinessUnits.raw<br>
    BusinessUnits.id<br>
    BusinessUnits.account_id<br>
    BusinessUnits.parent_id<br>
    BusinessUnits.name<br>
    BusinessUnits.description<br>
    BusinessUnits.path<br>
    BusinessUnits.created_at<br>
    BusinessUnits.updated_at'''
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__id = rawDict.get("id") or None
        self.__account_id = rawDict.get("account_id") or None
        self.__parent_id = rawDict.get("parent_id") or None
        self.__name = rawDict.get("name") or None
        self.__description = rawDict.get("description") or None
        self.__path = rawDict.get("path") or None
        self.__created_at = rawDict.get("created_at") or None
        self.__updated_at = rawDict.get("updated_at") or None

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def account_id(self):
        return self.__account_id
    @property
    def parent_id(self):
        return self.__parent_id
    @property
    def name(self):
        return self.__name
    @property
    def description(self):
        return self.__description
    @property
    def path(self):
        return self.__path
    @property
    def created_at(self):
        return self.__created_at
    @property
    def updated_at(self):
        return self.__updated_at

    @classmethod
    def getBusinessUnits(cls, token):
        '''Query all the business units in a specific BIM 360 account.
        Scope account:read'''
        checkScopes(token, "account:read")
        endpointUrl = "/hq/v1/accounts/{aId}/business_units_structure".format(aId=token.bimAccId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        if r == {}:
            raise AFWExceptions.APIError("No business units in this account.")
        else:
            return [cls(u) for u in r["business_units"]]

    @classmethod
    def createBusinessUnits(cls, token: client.Token, Data: list):
        '''Creates or redefines the business units of a specific BIM 360 account.
        Scope account:write
        Data: A list of dictionaries with the following structure. Name is mandatory
        'Data = [
                    {
                        "id": "933df8fd-abb2-4e4e-8f79-95ba2afebc6c",
                        "parent_id": null,
                        "name": "North America",
                        "description": "USA, Canada"
                    },
                    {
                        "id": "fda4ab9e-ab82-4ba9-8d6c-ae7dbd7cee31",
                        "parent_id": "933df8fd-abb2-4e4e-8f79-95ba2afebc6c",
                        "name": "USA Western Region",
                        "description": "California, Nevada, Washington"
                    }
                ]''' # TODO Maybe to cope with list of dicts, solution could be createBusinessUnit and silently call the batch __createBusinessUnits (this func)
        checkScopes(token, "account:read")
        endpointUrl = "/hq/v1/accounts/{aId}/business_units_structure".format(aId=token.bimAccId)
        bness = {"business_units": Data}
        r = requests.put(endpointUrl, headers=token.patchHeader, data=str(bness)).json()
        checkResponse(r)
        return [cls(u) for u in r["business_units"]]

class Jobs(object):
    '''Jobs.raw<br>
    Jobs.id<br>
    Jobs.account_id<br>
    Jobs.name<br>
    Jobs.status<br>
    Jobs.details'''
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__id = rawDict.get("id") or None
        self.__account_id = rawDict.get("account_id") or None
        self.__name = rawDict.get("name") or None
        self.__status = rawDict.get("status") or None
        self.__details = rawDict.get("details") or None

    @property
    def raw(self):
        return self.__raw
    @property
    def id(self):
        return self.__id
    @property
    def account_id(self):
        return self.__account_id
    @property
    def name(self):
        return self.__name
    @property
    def status(self):
        return self.__status
    @property
    def details(self):
        return self.__details

# pDocs ignore
__pdoc__ = {}
__pdoc__['Project.raw'] = False
__pdoc__['Project.id'] = False
__pdoc__['Project.accId'] = False    
__pdoc__['Project.name'] = False
__pdoc__['Project.start_date'] = False
__pdoc__['Project.end_date'] = False
__pdoc__['Project.project_type'] = False
__pdoc__['Project.value'] = False
__pdoc__['Project.currency'] = False
__pdoc__['Project.status'] = False
__pdoc__['Project.job_number'] = False
__pdoc__['Project.address_line_1'] = False
__pdoc__['Project.address_line_2'] = False
__pdoc__['Project.city'] = False
__pdoc__['Project.state_or_province'] = False
__pdoc__['Project.postal_code'] = False
__pdoc__['Project.country'] = False
__pdoc__['Project.business_unit_id'] = False
__pdoc__['Project.timezone'] = False
__pdoc__['Project.language'] = False
__pdoc__['Project.construction_type'] = False
__pdoc__['Project.contract_type'] = False
__pdoc__['Project.service_types'] = False
__pdoc__['Project.created_at'] = False
__pdoc__['Project.updated_at'] = False
__pdoc__['Project.include_companies'] = False
__pdoc__['Project.include_locations'] = False
__pdoc__['Project.template_project_id'] = False

__pdoc__['Company.raw'] = False
__pdoc__['Company.id'] = False
__pdoc__['Company.accId'] = False
__pdoc__['Company.name'] = False
__pdoc__['Company.trade'] = False
__pdoc__['Company.address_line_1'] = False
__pdoc__['Company.address_line_2'] = False
__pdoc__['Company.city'] = False
__pdoc__['Company.postal_code'] = False
__pdoc__['Company.state_or_province'] = False
__pdoc__['Company.country'] = False
__pdoc__['Company.phone'] = False
__pdoc__['Company.website_url'] = False
__pdoc__['Company.description'] = False
__pdoc__['Company.created_at'] = False
__pdoc__['Company.updated_at'] = False
__pdoc__['Company.erp_id'] = False
__pdoc__['Company.tax_id'] = False

__pdoc__['User.raw'] = False
__pdoc__['User.id'] = False
__pdoc__['User.account_id'] = False
__pdoc__['User.status'] = False
__pdoc__['User.role'] = False
__pdoc__['User.company_id'] = False
__pdoc__['User.company_name'] = False
__pdoc__['User.last_sign_in'] = False
__pdoc__['User.email'] = False
__pdoc__['User.name'] = False
__pdoc__['User.nickname'] = False
__pdoc__['User.first_name'] = False
__pdoc__['User.last_name'] = False
__pdoc__['User.uid'] = False
__pdoc__['User.image_url'] = False
__pdoc__['User.address_line_1'] = False
__pdoc__['User.address_line_2'] = False
__pdoc__['User.city'] = False
__pdoc__['User.postal_code'] = False
__pdoc__['User.state_or_province'] = False
__pdoc__['User.country'] = False
__pdoc__['User.phone'] = False
__pdoc__['User.company'] = False
__pdoc__['User.job_title'] = False
__pdoc__['User.industry'] = False
__pdoc__['User.about_me'] = False
__pdoc__['User.created_at'] = False
__pdoc__['User.updated_at'] = False

__pdoc__['IndustryRoles.raw'] = False
__pdoc__['IndustryRoles.id'] = False
__pdoc__['IndustryRoles.project_id'] = False
__pdoc__['IndustryRoles.name'] = False
__pdoc__['IndustryRoles.projectAdminAccess'] = False
__pdoc__['IndustryRoles.insightAccess'] = False
__pdoc__['IndustryRoles.docManagementAccess'] = False
__pdoc__['IndustryRoles.member_group_id'] = False

__pdoc__['BusinessUnits.raw'] = False
__pdoc__['BusinessUnits.id'] = False
__pdoc__['BusinessUnits.account_id'] = False
__pdoc__['BusinessUnits.parent_id'] = False
__pdoc__['BusinessUnits.name'] = False
__pdoc__['BusinessUnits.description'] = False
__pdoc__['BusinessUnits.path'] = False
__pdoc__['BusinessUnits.created_at'] = False
__pdoc__['BusinessUnits.updated_at'] = False

__pdoc__['Jobs.raw'] = False
__pdoc__['Jobs.id'] = False
__pdoc__['Jobs.account_id'] = False
__pdoc__['Jobs.name'] = False
__pdoc__['Jobs.status'] = False
__pdoc__['Jobs.details'] = False

# TODO Try string dictionaries with import companies. critical - OPTIONS CLASS
# TODO change dictionary templates with "options" class. Maybe "AfwOptions" or "ForgeOptions" or "CreationOptions"
# TODO json.dumps(data) to all options for requests data
# TODO Remove all client parameters. client information is included in the Token now

# Account Admin
# Projects
# PATCH projects/:project_id/image

# Companies
# POST companies/import NOT WORKING?

# PATCH companies/:company_id/image

# Account Users
# POST users
# POST users/import
# GET users/search
