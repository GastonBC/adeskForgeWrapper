# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API

**Installation** `pip install adeskForgeWrapper`

**API Reference** [https://gastonbc.github.io/index.html](https://gastonbc.github.io/index.html)

There are currently 3 modules implemented: [Bim360](https://gastonbc.github.io/B360.html), [Data Management](https://gastonbc.github.io/DM.html) and [Token Flex](https://gastonbc.github.io/TokenFlex.html)
##
### Setting up credentials and getting a 2 legged token
Notice we will use *cli* and *token* in most methods
```Python
import adeskForgeWrapper as afw

#Your Forge app credentials, strings in every field
forgeCliId = 'FORGE_CLIENT_ID'
forgeCliSec = 'FORGE_CLIENT_SECRET'

# Your B360 hub ID and name
B360AccId = 'BIM360_ACC_ID'
B360AccName = 'BIM360_ACC_NAME'

# We are going to need both of these in most methods
cli = afw.client.Client(forgeCliId, forgeCliSec, B360AccId, B360AccName)
token = afw.client.Token.get2LeggedToken("account:read", cli)
```
### Getting a 3 legged token
Some methods require an authentication process, for example those in the Token Flex module.
```Python
# We will need to provide a callback URL, this one needs to be the same 
# url you used to register your Forge app

callbackUrl ="https://dashboard.archsourcing.com"

cli = afw.client.Client(forgeCliId, forgeCliSec, B360AccId, B360AccName)

# Provide the URL in the method and copy the full 
# response URL you are taken to after logging

token = afw.client.Token.get3LeggedToken("data:read", cli, callbackUrl)
```

### Retrieve all projects in the your Hub
```Python
projs = afw.B360.Project.getProjects(cli, token)

# Print some properties
for p in projs:
    print(p.name)
    print(p.id)
```
### Get project by ID
```Python
p = afw.b360.Project.getProjectById(cli, token, "PROJECT_ID")
```
### Get all users in the project
```Python
users = p.getUsersFromProject(token)
```
### Get companies in your hub
```Python
comps = afw.B360.Company.getCompanies(cli, token)
# Again, you can print their properties
for company in comps:
    print(company.name)
    print(company.id)
    print(company.country)
```

### Now something more complex, updating a project
```Python
# Get your project, we need multiple scopes for this
# notice the scopes separated by a space
token = afw.client.Token("account:read account:write", cli)

proj = afw.B360.Project.getProjectById(cli, token, "PROJECT_ID")

# Update it, Data is a dictionary with the properties 
# you want to update the template is in the docstring

Data = {
	"name" : "afwExample",
	"status" : "active",
       }

updatedProject = proj.updateProject(token, Data)

# Updated properties
print(updatedProject.name)
print(updatedProject.status)
```
##### ***This is a work in progress***
