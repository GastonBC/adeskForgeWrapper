# ----------
# Wrapper for BIM360 API
# https://forge.autodesk.com/en/docs/bim360/v1/reference/http/
# ----------
'''Module for the BIM 360 API'''

import requests

from . import AFWExceptions
from . import client
from .utils import checkScopes
from .utils import checkResponse
from . import utils
from .utils import AUTODESK_BASE_URL as BASE_URL
import json


class Options(object):
    '''Some methods require data and parameters in diferent formats, 
    this class makes it easy to add those and ensures the information is sent the right way.'''

    @staticmethod
    def create_project_options(name, start_date, end_date, project_type, value, currency, **kwargs):
        '''Options for  `Project.create_roject`<br>
        Note that NAME, START_DATE, END_DATE, PROJECT_TYPE, VALUE and CURRENCY are required values.<br>
        name<br>
        start_date - YYYY-MM-DD<br>
        end_date - YYYY-MM-DD, later than start date<br>
        project_type - Refer to parameters (https://forge.autodesk.com/en/docs/bim360/v1/overview/parameters/)<br>
        currency - Refer to parameters<br>
        language - Refer to parameters<br><br>
        
        kwargs:<br>
        service_types<br>
        job_number<br>
        address_line_1<br>
        address_line_2<br>
        city<br>
        state_or_province<br>
        postal_code<br>
        country<br>
        business_unit_id<br>
        timezone<br>
        language - Refer to parameters<br>
        construction_type<br>
        contract_type<br>
        template_project_id<br>
        include_companies<br>
        include_locations<br>'''
        
        allowedKwgs = ["service_types", "job_number", "address_line_1", "address_line_2", 
                       "city", "state_or_province", "postal_code", "country", "business_unit_id",
                       "timezone", "language", "construction_type", "contract_type", 
                       "template_project_id", "include_companies", "include_locations"]
        utils.allowed_kwargs_check(allowedKwgs, kwargs)
        
        data = {
            "name":name,
            "start_date":start_date,
            "end_date":end_date,
            "project_type":project_type, 
            "value":value,
            "currency":currency,
            "service_types":kwargs.get("service_types", None),
            "job_number":kwargs.get("job_number", None),
            "address_line_1":kwargs.get("address_line_1", None),
            "address_line_2":kwargs.get("address_line_2", None),
            "city":kwargs.get("city", None),
            "state_or_province":kwargs.get("state_or_province", None),
            "postal_code":kwargs.get("postal_code", None),
            "country":kwargs.get("country", None),
            "business_unit_id":kwargs.get("business_unit_id", None),
            "timezone":kwargs.get("timezone", None),
            "language":kwargs.get("language", None),
            "construction_type":kwargs.get("construction_type", None),
            "contract_type":kwargs.get("contract_type", None)
        }
        data = {k : v for k,v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def update_project_options(**kwargs):
        '''Options for `Project_update_project`<br><br>

        kwargs:<br>
        name<br>
        start_date - YYYY-MM-DD<br>
        end_date - YYYY-MM-DD, later than start date<br>
        project_type - Refer to parameters (https://forge.autodesk.com/en/docs/bim360/v1/overview/parameters/)<br>
        currency - Refer to parameters<br>
        language - Refer to parameters<br><br>
        service_types<br>
        job_number<br>
        address_line_1<br>
        city<br>
        state_or_province<br>
        postal_code<br>
        country<br>
        business_unit_id<br>
        timezone<br>
        language - Refer to parameters<br>
        construction_type<br>
        contract_type<br>
        template_project_id<br>
        include_companies<br>
        include_locations<br>
        '''
        data = {
            "name":kwargs.get("name", None),
            "status":kwargs.get("status", None),
            "start_date":kwargs.get("start_date", None),
            "end_date":kwargs.get("end_date", None),
            "project_type":kwargs.get("project_type", None),
            "value":kwargs.get("value", None),
            "currency":kwargs.get("currency", None),
            "service_types":kwargs.get("service_types", None),
            "job_number":kwargs.get("job_number", None),
            "address_line_1":kwargs.get("address_line_1", None),
            "address_line_2":kwargs.get("address_line_2", None),
            "city":kwargs.get("city", None),
            "state_or_province":kwargs.get("state_or_province", None),
            "postal_code":kwargs.get("postal_code", None),
            "country":kwargs.get("country", None),
            "business_unit_id":kwargs.get("business_unit_id", None),
            "timezone":kwargs.get("timezone", None),
            "language":kwargs.get("language", None),
            "construction_type":kwargs.get("construction_type", None),
            "contract_type":kwargs.get("contract_type", None)
        }
        
        data = {k : v for k,v in data.items() if v is not None} 
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def export_PDF_options(versionId, includeMarkups = False, includeHyperlinks = False):
        '''Options to export PDFs'''
        if type(includeMarkups) != bool or type(includeMarkups) != bool:
            raise TypeError("includeMarkups/includeHyperlinks expected bool")
        data={"includeMarkups": includeMarkups,
              "includeHyperlinks": includeHyperlinks}
        return (versionId, data)

    @staticmethod
    def update_user_options(status, company_id):
        '''Options to update a user'''
        data = {
                "status": status,
                "company_id": company_id
                }
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def update_company_options(**kwargs):
        '''Options for updateCompany<br><br>
        
        kwargs:<br>
        name<br>
        trade<br>
        address_line_1<br>
        address_line_2<br>
        city<br>
        state_or_province<br>
        country<br>
        phone<br>
        website_url<br>
        description<br>
        erp_id<br>
        tax_id'''
        
        data = {"name":kwargs.get("name", None),
                "trade":kwargs.get("trade", None),
                "address_line_1":kwargs.get("address_line_1", None),
                "address_line_2":kwargs.get("address_line_2", None),
                "city":kwargs.get("city", None),
                "state_or_province":kwargs.get("state_or_province", None),
                "country":kwargs.get("country", None),
                "phone":kwargs.get("phone", None),
                "website_url":kwargs.get("website_url", None),
                "description":kwargs.get("description", None),
                "erp_id":kwargs.get("erp_id", None),
                "tax_id":kwargs.get("tax_id", None)
                }
        data = {k : v for k,v in data.items() if v is not None} 
        return json.dumps(data, ensure_ascii=True)

    @staticmethod
    def search_companies_options(**kwargs):
        '''Options for searchCompany<br><br>
        
        kwargs:<br>
        name<br>
        trade<br>
        operator<br>
        partial<br>
        limit<br>
        offset<br>
        sort<br>
        field'''
        params = (
                ('name', kwargs.get("name", None)),
                ('trade', kwargs.get("trade", None)),
                ('operator', kwargs.get("operator", None)),
                ('partial', kwargs.get("partial", None)),
                ('limit', kwargs.get("limit", None)),
                ('offset', kwargs.get("offset", None)),
                ('sort', kwargs.get("sort", None)),
                ('field', kwargs.get("field", None))
                )
        return params

    @staticmethod
    def add_user_options(**kwargs):
        '''Use this method for each user you want to update<br><br>

        kwargs:<br>
        email<br>
        user_id<br>
        docManagementAccessLevel<br>
        projectAdminAccessLevel<br>
        projectAdminAccessLevel<br>
        industry_roles<br>
        '''
        data={
            "email": kwargs.get("email", None),
            "user_id": kwargs.get("user_id", None),
            "services": {
                        "document_management": {"access_level": kwargs.get("docManagementAccessLevel", None)},
                        "project_administration": {"access_level": kwargs.get("projectAdminAccessLevel", None)},
                        },
            "company_id":kwargs.get("company_id", None),
            "industry_roles":kwargs.get("industry_roles", None)
            }
        return data

    @staticmethod
    def import_company_options(name, trade, **kwargs):
        '''Use this method for each company you want to update and pass a list to import_companies<br><br>
        
        kwargs:<br>
        website_url<br>
        city<br>
        country<br>
        address_line_1<br>
        address_line_2<br>
        postal_code<br>
        erp_id<br>
        tax_id<br>
        phone<br>
        description
        '''
        allowedKwgs = ['website_url', 'city', 'country', 'address_line_1', 'address_line_2',
                       'postal_code', 'erp_id', 'tax_id', 'phone', 'description']
        utils.allowed_kwargs_check(allowedKwgs, kwargs)

        data = {
                "name": name,
                "trade": trade,
                "website_url": kwargs.get('website_url', None),
                "city": kwargs.get('city', None),
                "country": kwargs.get('country', None),
                "address_line_1": kwargs.get('address_line_1', None),
                "address_line_2": kwargs.get('address_line_2', None),
                "postal_code": kwargs.get('postal_code', None),
                "erp_id": kwargs.get('erp_id', None),
                "tax_id": kwargs.get('tax_id', None),
                "phone": kwargs.get('phone', None),
                "description": kwargs.get('description', None)
                }

        return json.dumps(data, ensure_ascii=True)

 
class Project(object):
#hiddenRegion
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

    def __init__(self, rawDict):
        self._raw = rawDict

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def account_id(self):
        return self._raw.get("account_id", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def start_date(self):
        return self._raw.get("start_date", None)
    @property
    def end_date(self):
        return self._raw.get("end_date", None)
    @property
    def project_type(self):
        return self._raw.get("project_type", None)
    @property
    def value(self):
        return self._raw.get("value", None)
    @property
    def currency(self):
        return self._raw.get("currency", None)
    @property
    def status(self):
        return self._raw.get("status", None)
    @property
    def job_number(self):
        return self._raw.get("job_number", None)
    @property
    def address_line_1(self):
        return self._raw.get("address_line_1", None)
    @property
    def address_line_2(self):
        return self._raw.get("address_line_2", None)
    @property
    def city(self):
        return self._raw.get("city", None)
    @property
    def state_or_province(self):
        return self._raw.get("state_or_province", None)
    @property
    def postal_code(self):
        return self._raw.get("postal_code", None)
    @property
    def country(self):
        return self._raw.get("country", None)
    @property
    def business_unit_id(self):
        return self._raw.get("business_unit_id", None)
    @property
    def timezone(self):
        return self._raw.get("timezone", None)
    @property
    def language(self):
        return self._raw.get("language", None)
    @property
    def construction_type(self):
        return self._raw.get("construction_type", None)
    @property
    def contract_type(self):
        return self._raw.get("contract_type", None)
    @property
    def last_sign_in(self):
        return self._raw.get("last_sign_in", None)
    @property
    def service_types(self):
        return self._raw.get("service_types", None)
    @property
    def created_at(self):
        return self._raw.get("created_at", None)
    @property
    def updated_at(self):
        return self._raw.get("updated_at", None)
#endRegion

    @classmethod
    def get_projects(cls, token: client.Token):
        '''Query all the projects in a specific BIM 360 account.<br>
        Scope - account:read<br>
        Returns a list of project objects.'''
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/projects".format(aId=token.bim_account_id)
        checkScopes(token, "account:read")
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [cls(p) for p in r]

    @classmethod
    def project_by_id(cls, token: client.Token, p_id):
        '''Query the details of a specific BIM 360 project.<br>
        Scope: account:read'''
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/projects/{pId}".format(aId=token.bim_account_id, pId=p_id)
        checkScopes(token, "account:read")
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def create_project(cls, token: client.Token, create_project_options):
        '''Create a new BIM 360 project in a specific BIM 360 account.<br>
        Scope - `account:write`<br>
        creationOps - From Options Class, createProjectOptions()'''
        checkScopes(token, "account:write")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/projects".format(aId=token.bim_account_id)
        r = requests.post(endpoint_url, headers=token.patch_header, data=create_project_options).json()
        print(r)
        checkResponse(r)
        return cls(r)

    def update_project(self, token: client.Token, update_project_options):
        '''Update the properties of only the specified attributes of a specific BIM 360 project.<br>
           Scope - `account:write account:read`'''
        checkScopes(token, "account:read account:write")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/projects/{pId}".format(aId=self.account_id, pId=self.id)
        r = requests.patch(endpoint_url, headers=token.patch_header, data=update_project_options).json()
        checkResponse(r)
        return Project(r)
    
    def get_users(self, token: client.Token):
        '''Retrieves information about all the users in a project.<br>
        To get information about all the users in an account, see GET accounts/users.<br>
        Scope - account:read'''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/bim360/admin/v1/projects/{pId}/users".format(pId=self.id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [User(u) for u in r["results"]]

    def user_by_id(self, token: client.Token, user_id):
        '''Retrieves detailed information about a single user in a project.<br>
        Scope - account:read'''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/bim360/admin/v1/projects/{pId}/users/{uId}".format(pId=self.id, uId=user_id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return User(r)

    def add_users(self, token: client.Token, add_user_options: list):
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
        if type(add_user_options) != list:
            raise AFWExceptions.AFWError("add_user_options must be a list of Options.add_user_options")
        checkScopes(token, "account:write")

        add_user_options = json.dumps(add_user_options)
        endpoint_url = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/users/import".format(
            aId=self.account_id ,pId=self.id)

        r = requests.post(endpoint_url, headers=token.content_x_user, data=add_user_options).json()
        checkResponse(r)
        print("Success:", r["success"])
        print("Failed:", r["failure"])
        return [User.user_by_id(token, u["user_id"]) for u in r["success_items"]]

    def update_user_by_id(self, token: client.Token, user_id, update_user_options):
        '''Updates a user’s profile for a project, including:<br><br>

        The company the user is assigned to for the project.<br>
        The industry roles assigned to the user for the project.<br><br>
        Scope - account:write
        
        Returns a User object'''
        # TODO: Thinking about changing user id with user object, updating 
        # the user object with the response

        checkScopes(token, "account:write")

        endpoint_url = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/users/{uId}".format(
            aId=self.account_id ,pId=self.id, uId=user_id)

        r = requests.patch(endpoint_url, headers=token.content_x_user, data=update_user_options).json()
        checkResponse(r)
        return User(r)

    def industry_roles(self, token: client.Token):
        '''Retrieves the industry roles for the project. For example, contractor and architect.<br>
        Scope - account:read'''

        checkScopes(token, "account:read")

        endpoint_url = BASE_URL+"/hq/v2/accounts/{aId}/projects/{pId}/industry_roles".format(
            aId=self.account_id ,pId=self.id)

        r = requests.get(endpoint_url, headers=token.patch_header).json()
        checkResponse(r)
        return [IndustryRoles(i) for i in r]

    def export_PDF(self, token: client.Token, export_PDF_options):
        '''Exports a single page from an uploaded PDF file into a new PDF file.<br>
            You can also export the page’s markups (annotations) and hyperlinks.<br>
            Scope - data:read<br>
            exportOptions - exportPDFOptions()<br>
            Note that you can only export a page from a PDF file that was uploaded to the 
            Plans folder or to a folder nested under the Plans folder 
            (attributes.extension.data.actions: SPLIT). BIM 360 Document Management 
            splits these files into separate pages (sheets) when they are uploaded, 
            and assigns a separate ID to each page.<br>
            You can identify exportable PDF files, by searching for files with the 
            following combmination of properties:<br><br>

            attributes.extension.type: items:autodesk.bim360.Document 
            (identifies all files that are split into separate pages)<br>
            attributes.extension.data.sourceFileName: <filename>.pdf 
            (identifies all PDF files)<br>
            You can export PDF pages both from PDF files that were uploaded via the 
            BIM 360 Document Management UI and from PDF files that were uploaded via 
            BIM 360 endpoints. For more details about uploading documents to BIM 360 via the 
            BIM 360 endpoints, see the File Upload tutorial.<br><br>

            Note that this endpoint is asynchronous and initiates a job that 
            runs in the background, rather than halting execution of your program.<br>
            The response returns an export ID that you can use to call getPDFExport() 
            to verify the status of the job. When the job is complete, you can retrieve 
            the data you need to download the exported page.<br><br>

            Note that the user must have permission to view files. For information about 
            permissions, see the Help documentation.<br><br>

            For more details about exporting PDF files, see the PDF Export tutorial.<br><br>

            For more information about Document Management endpoints, see 
            the Data Management API<br><br>
            '''

        checkScopes(token, "data:read")
        endpoint_url = BASE_URL+"/bim360/docs/v1/projects/{pId}/versions/{vId}/exports".format(
            pId=self.id, vId=export_PDF_options[0])

        r = requests.post(endpoint_url, 
                          headers=token.patch_header, 
                          data=str(export_PDF_options[1])).json()
        checkResponse(r)
        print("Id: {id}\nStatus: {status}".format(id=r["id"], status=r["status"]))
        return r

    def get_PDF_export(self, token: client.Token, versionId: str, exportId: str):
        '''Returns the status of a PDF export job, as well as data you need to download 
        the exported file when the export is complete.<br>
            The exportPDF() function initiates the job, and returns a job ID to be used 
            in this endopint.<br>
            To download the exported PDF file after the job is complete, 
            use GET :urn/manifest/:derivativeurn.<br><br>
            
            For more information about Document Management endpoints, see the Data Management API'''
            # TODO: Model derivative api function here

        checkScopes(token, "data:read")

        urlEnd = "/bim360/docs/v1/projects/{pId}/versions/{vId}/exports/{eId}".format(
            pId=self.id, vId=versionId, eId=exportId)

        endpoint_url = BASE_URL + urlEnd
        r = requests.get(endpoint_url, headers=token.content_x_user).json()
        checkResponse(r)
        print(r) #TODO: Try, .json() may not work here. will probably find a way once 
                 # model derivative api is running.
                 #TODO: Range header
        return r


class Company(object):
#hiddenRegion
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

    def __init__(self, rawDict):
        self._raw = rawDict

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def account_id(self):
        return self._raw.get("account_id", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def trade(self):
        return self._raw.get("trade", None)
    @property
    def address_line_1(self):
        return self._raw.get("address_line_1", None)
    @property
    def address_line_2(self):
        return self._raw.get("address_line_2", None)
    @property
    def city(self):
        return self._raw.get("city", None)
    @property
    def postal_code(self):
        return self._raw.get("postal_code", None)
    @property
    def state_or_province(self):
        return self._raw.get("state_or_province", None)
    @property
    def country(self):
        return self._raw.get("country", None)
    @property
    def phone(self):
        return self._raw.get("phone", None)
    @property
    def website_url(self):
        return self._raw.get("website_url", None)
    @property
    def description(self):
        return self._raw.get("description", None)
    @property
    def created_at(self):
        return self._raw.get("created_at", None)
    @property
    def updated_at(self):
        return self._raw.get("updated_at", None)
    @property
    def erp_id(self):
        return self._raw.get("erp_id", None)
    @property
    def tax_id(self):
        return self._raw.get("tax_id", None)
#endRegion

    @classmethod
    def company_by_id(cls, token: client.Token, c_id):
        '''Query the details of a specific partner company.<br>
        Scope: account:read'''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/companies/{cId}".format(
            aId=token.bim_account_id, cId=c_id)

        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def get_companies(cls, token: client.Token):
        '''Query all the partner companies in a specific BIM 360 account.<br>
        Scope account:read'''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/companies".format(aId=token.bim_account_id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [cls(c) for c in r]

    @classmethod
    def searchCompaniesByName(cls, token: client.Token, searchOps):
        '''Search partner companies in a specific BIM 360 account by name.<br>
        Scope - account:read<br>
        searchOps - Options.searchCompaniesOptions()
        '''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/companies/search".format(
            aId=token.bim_account_id)

        r = requests.get(endpoint_url, headers=token.get_header, params=searchOps).json()
        checkResponse(r)
        if r == []:
            return None
        else:
            return [cls(c) for c in r]

    @classmethod
    def import_companies(cls, token: client.Token, data):
        '''Bulk import partner companies to the company directory in a 
        specific BIM 360 account.<br>
        (50 companies maximum can be included in each call.)<br>
        Scope - account:write<br>
        data - Options.import_company_options() list
        '''
        checkScopes(token, "account:write")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/companies/import".format(
            aId=token.bim_account_id)

        r = requests.post(endpoint_url, headers=token.patch_header,data=data).json()
        checkResponse(r)
        print("Success:", r["success"])
        print("Failure:", r["failure"])
        return [cls(c) for c in r["success_items"]]

    def updateCompany(self, token: client.Token, updateCompanyOptions):
        '''Update the properties of only the specified attributes of a specific partner company.<br>
        Scope - account:write'''
        checkScopes(token, "account:write")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/companies/{cId}".format(
            aId=self.account_id, cId=self.id)

        r = requests.patch(endpoint_url, 
                           headers=token.patch_header,
                           data=updateCompanyOptions).json()
        checkResponse(r)
        return Company(r)


class User(object):
#hiddenRegion
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

    def __init__(self, rawDict):
        self._raw = rawDict
        
    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def account_id(self):
        return self._raw.get("account_id", None)
    @property
    def status(self):
        return self._raw.get("status", None)
    @property
    def role(self):
        return self._raw.get("role", None)
    @property
    def company_id(self):
        return self._raw.get("company_id", None)
    @property
    def company_name(self):
        return self._raw.get("company_name", None)
    @property
    def last_sign_in(self):
        return self._raw.get("last_sign_in", None)
    @property
    def email(self):
        return self._raw.get("email", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def nickname(self):
        return self._raw.get("nickname", None)
    @property
    def first_name(self):
        return self._raw.get("first_name", None)
    @property
    def last_name(self):
        return self._raw.get("last_name", None)
    @property
    def uid(self):
        return self._raw.get("uid", None)
    @property
    def image_url(self):
        return self._raw.get("image_url", None)
    @property
    def address_line_1(self):
        return self._raw.get("address_line_1", None)
    @property
    def address_line_2(self):
        return self._raw.get("address_line_2", None)
    @property
    def city(self):
        return self._raw.get("city", None)
    @property
    def postal_code(self):
        return self._raw.get("postal_code", None)
    @property
    def state_or_province(self):
        return self._raw.get("state_or_province", None)
    @property
    def country(self):
        return self._raw.get("country", None)
    @property
    def phone(self):
        return self._raw.get("phone", None)
    @property
    def company(self):
        return self._raw.get("company", None)
    @property
    def job_title(self):
        prop = self._raw.get("job_title", None) or self._raw.get("jobTitle", None)
        return prop
    @property
    def industry(self):
        return self._raw.get("industry", None)
    @property
    def about_me(self):
        return self._raw.get("about_me", None)
    @property
    def created_at(self):
        return self._raw.get("created_at", None)
    @property
    def updated_at(self):
        return self._raw.get("updated_at", None)
#endRegion

    @classmethod
    def users_from_account(cls, token: client.Token):
        '''Query all the users in a specific BIM 360 account.<br>
        Scope account:read'''
        checkScopes(token, "account:read")
        endpoint_url = BASE_URL+"/hq/v1/accounts/{aId}/users".format(aId=token.bim_account_id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [cls(u) for u in r]

    @classmethod
    def user_by_id(cls, token: client.Token, user_id):
        '''Query the details of a specific user.<br>
        Scope `account:read'''
        checkScopes(token, "account:read")
        endpoint_url = "/hq/v1/accounts/{aId}/users/{uId}".format(
            aId=token.bim_account_id, uId=user_id)

        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return cls(r)

    @classmethod
    def update_user_by_id(cls, token: client.Token, user_id, update_user_options):
        '''Update a specific user’s status or default company. Data template below<br>
        Scope - account:write<br>
        updateUserOptions - From Options class'''
        checkScopes(token, "account:write")
        endpoint_url = "/hq/v1/accounts/{aId}/users/{uId}".format(aId=token.bim_account_id, uId=user_id)

        r = requests.patch(endpoint_url,
                           headers=token.patch_header,
                           data=update_user_options).json()

        checkResponse(r)
        return cls(r)

    def update_user(self, token: client.Token, update_user_options):
        '''Update a specific user’s status or default company. Data template below<br>
        Scope - account:write<br>
        updateUserOptions - From Options class'''
        checkScopes(token, "account:write")
        endpoint_url = "/hq/v1/accounts/{aId}/users/{uId}".format(
            aId=token.bim_account_id, uId=self.id)

        r = requests.patch(endpoint_url,
                           headers=token.patch_header,
                           data=update_user_options).json()
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
        self._raw = rawDict

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def project_id(self):
        return self._raw.get("project_id", None)
    @property
    def projectAdminAccess(self):
        return self._raw["services"]["project_administration"].get("access_level", None)
    @property
    def insightAccess(self):
        return self._raw.get["services"]["insight"].get("access_level", None)
    @property
    def docManagementAccess(self):
        return self._raw["services"]["document_management"].get("access_level", None)
    @property
    def member_group_id(self):
        return self._raw.get("member_group_id", None)


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
        self._raw = rawDict

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def account_id(self):
        return self._raw.get("account_id", None)
    @property
    def parent_id(self):
        return self._raw.get("parent_id", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def description(self):
        return self._raw.get("description", None)
    @property
    def path(self):
        return self._raw.get("path", None)
    @property
    def created_at(self):
        return self._raw.get("created_at", None)
    @property
    def updated_at(self):
        return self._raw.get("updated_at", None)

    @classmethod
    def get_business_units(cls, token):
        '''Query all the business units in a specific BIM 360 account.
        Scope account:read'''
        checkScopes(token, "account:read")
        endpoint_url = "/hq/v1/accounts/{aId}/business_units_structure".format(aId=token.bim_account_id)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        if r == {}:
            raise AFWExceptions.APIError("No business units in this account.")
        else:
            return [cls(u) for u in r["business_units"]]

    @classmethod
    def create_business_units(cls, token: client.Token, Data: list):
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
                ]''' # TODO Maybe to cope with list of dicts, solution could be 
                     # createBusinessUnit and silently call the 
                     # batch _createBusinessUnits (this func)

        checkScopes(token, "account:read")
        endpoint_url = "/hq/v1/accounts/{aId}/business_units_structure".format(aId=token.bim_account_id)
        bness = {"business_units": Data}
        r = requests.put(endpoint_url, headers=token.patch_header, data=str(bness)).json()
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
        self._raw = rawDict or None

    @property
    def raw(self):
        return self._raw
    @property
    def id(self):
        return self._raw.get("id", None)
    @property
    def account_id(self):
        return self._raw.get("account_id", None)
    @property
    def name(self):
        return self._raw.get("name", None)
    @property
    def status(self):
        return self._raw.get("status", None)
    @property
    def details(self):
        return self._raw.get("details", None)

# pdocs ignore
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
# TODO is it worth to check kwargs?
# TODO add backticks ` to funcs 

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