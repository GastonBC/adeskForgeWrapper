# ----------
# Wrapper for Token Flex API
# https://forge.autodesk.com/en/docs/tokenflex/v1/
# ----------

import requests

from .utils import TOKENFLEX_API
from .utils import checkScopes
from .utils import checkResponse
from . import client


'''Tokens in this module must be 3 legged. Check client.get3LeggedToken()'''
class Contract(object):
    '''Contract.raw<br>
    Contract.contractNumber<br>
    Contract.contractName<br>
    Contract.contractStartDate<br>
    Contract.contractEndDate<br>
    Contract.multiyearProvisionedTokens<br>
    Contract.contractYears<br>
    Contract.isActive'''
#HiddenRegion
    def __init__(self, rawDict):
        self.__raw = rawDict or None
        self.__contractNumber = rawDict.get("contractNumber") or None
        self.__contractName = rawDict.get("contractName") or None
        self.__contractStartDate = rawDict.get("contractStartDate") or None
        self.__contractEndDate = rawDict.get("contractEndDate") or None
        self.__multiyearProvisionedTokens = rawDict.get("multiyearProvisionedTokens") or None
        self.__contractYears = rawDict.get("contractYears") or None
        self.__isActive = rawDict.get("isActive") or None

    @property
    def raw(self):
        return self.__raw
    @property
    def contractNumber(self):
        return self.__contractNumber
    @property
    def contractName(self):
        return self.__contractName
    @property
    def contractStartDate(self):
        return self.__contractStartDate
    @property
    def contractEndDate(self):
        return self.__contractEndDate
    @property
    def multiyearProvisionedTokens(self):
        return self.__multiyearProvisionedTokens
    @property
    def contractYears(self):
        return self.__contractYears
    @property
    def isActive(self):
        return self.__isActive
#endRegion

    @classmethod
    def getContracts(cls, token: client.Token):
        '''List all the accessible contracts and high level information for each contract.<br>
        The token must be obtained via 3-legged workflow. client.get3LeggedToken()<br>
        Scope data:read'''
        checkScopes(token, "data:read")
        endpointUrl = TOKENFLEX_API+"/contract"
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return [cls(c) for c in r]
    
    @classmethod
    def getContractById(cls, token: client.Token, contractId):
        '''Query details of a contract.<br>
        The token must be obtained via 3-legged workflow. client.get3LeggedToken()<br>
        This gives more details such as multiyear tokens, and contract details by year.<br>
        Scope data:read<br>'''
        checkScopes(token, "data:read")
        endpointUrl = TOKENFLEX_API+"/contract/{conId}".format(contractId)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return cls(r)

    def getEnrichmentCategories(self, token: client.Token):
        '''List all customer uploaded enrichment categories.<br>
        Returns a list with all enrichment categories of a contract.'''
        checkScopes(token, "data:read")
        endpointUrl = TOKENFLEX_API+"/contract/{conId}/enrichment".format(self.contractNumber)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return r

    def getEnrichmentValues(self, token: client.Token, category: str):
        '''Get all the unique values for an enrichment category.<br>
        Returns a list with all possible values for an enrichment category.'''
        checkScopes(token, "data:read")
        endpointUrl = TOKENFLEX_API+"/contract/{conId}/enrichment/{enrCat}".format(conId=self.contractNumber, enrCat=category)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return r

    def contractSummary(self, token: client.Token, filters = None):
        '''Get usage summary at a monthly aggregate level with the option of some filters. This method is recommended over 
        an ad-hoc query because this API returns data faster.<br>
        Returns a list of attributes'''
        checkScopes(token, "data:read")
        endpointUrl = TOKENFLEX_API+"/usage/{conId}/summary".format(conId = self.contractNumber)
        r = requests.get(endpointUrl, headers=token.getHeader).json()
        checkResponse(r)
        return r

__pdoc__ = {}
__pdoc__['Contract.raw'] = False
__pdoc__['Contract.contractNumber'] = False
__pdoc__['Contract.contractName'] = False
__pdoc__['Contract.contractStartDate'] = False
__pdoc__['Contract.contractEndDate'] = False
__pdoc__['Contract.multiyearProvisionedTokens'] = False
__pdoc__['Contract.contractYears'] = False
__pdoc__['Contract.isActive'] = False