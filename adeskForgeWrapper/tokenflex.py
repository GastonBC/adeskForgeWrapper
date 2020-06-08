# ----------
# Wrapper for TOKEN FLEX API
# https://forge.autodesk.com/en/docs/tokenflex/v1/
# ----------
'''Module for the Token Flex API<br>
Tokens in this module must be 3 legged. Check client.get3LeggedToken()'''

import requests

from .utils import TOKENFLEX_API
from .utils import checkScopes
from .utils import checkResponse
from . import client



class Contract(object):
#HiddenRegion
    '''Contract.raw<br>
    Contract.contractNumber<br>
    Contract.contractName<br>
    Contract.contractStartDate<br>
    Contract.contractEndDate<br>
    Contract.multiyearProvisionedTokens<br>
    Contract.contractYears<br>
    Contract.isActive'''
    def __init__(self, rawDict):
        self._raw = rawDict or None
    @property
    def raw(self):
        return self._raw
    @property
    def contractNumber(self):
        return self._raw.get("contractNumber", None)
    @property
    def contractName(self):
        return self._raw.get("contractName", None)
    @property
    def contractStartDate(self):
        return self._raw.get("contractStartDate", None)
    @property
    def contractEndDate(self):
        return self._raw.get("contractEndDate", None)
    @property
    def isActive(self):
        return self._raw.get("isActive", None)
#endRegion

    @classmethod
    def get_contracts(cls, token):
        '''List all the accessible contracts and high level information for each contract.<br>
        Token - Must be obtained via 3-legged workflow. client.get3LeggedToken()<br>
        Scope data:read'''
        checkScopes(token, "data:read")
        endpoint_url = TOKENFLEX_API+"/contract"
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return [cls(c) for c in r]
    
    @classmethod
    def contract_by_id(cls, token, contractId):
        '''Query details of a contract.<br>
        The token must be obtained via 3-legged workflow. client.get3LeggedToken()<br>
        This gives more details such as multiyear tokens, and contract details by year.<br>
        Scope data:read'''
        checkScopes(token, "data:read")
        endpoint_url = TOKENFLEX_API+"/contract/{conId}".format(contractId)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return cls(r)

    def get_enrichment_categories(self, token):
        '''List all customer uploaded enrichment categories.<br>
        Returns a list with all enrichment categories of a contract.'''
        checkScopes(token, "data:read")
        endpoint_url = TOKENFLEX_API+"/contract/{conId}/enrichment".format(self.contractNumber)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return r

    def get_enrichment_values(self, token, category):
        '''Get all the unique values for an enrichment category.<br>
        Returns a list with all possible values for an enrichment category.'''
        checkScopes(token, "data:read")
        endpoint_url = TOKENFLEX_API+"/contract/{conId}/enrichment/{enrCat}".format(conId=self.contractNumber, enrCat=category)
        r = requests.get(endpoint_url, headers=token.get_header).json()
        checkResponse(r)
        return r

    def contract_summary(self, token, filters = None):
        '''Get usage summary at a monthly aggregate level with the option of some filters. This method is recommended over 
        an ad-hoc query because this API returns data faster.<br>
        Returns a list of attributes'''
        checkScopes(token, "data:read")
        endpoint_url = TOKENFLEX_API+"/usage/{conId}/summary".format(conId = self.contractNumber)
        r = requests.get(endpoint_url, headers=token.get_header).json()
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