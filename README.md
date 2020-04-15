# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API

### Setting up credentials and getting a 2 legged token
Notice we will use *cli* and *token* in most methods
```Python
import adeskForgeWrapper as afw
import os

#Your Forge app credentials
forgeCliId = os.getenv('FORGE_CLIENT_ID')
forgeCliSec = os.getenv('FORGE_CLIENT_SECRET')

# Your B360 hub ID and name
B360AccId = os.getenv('BIM360_ACC_ID')
B360AccName = os.getenv('BIM360_ACC_NAME')

# We are going to need both of these in most methods
cli = afw.client.Client(forgeCliId, forgeCliSec, B360AccId, B360AccName)
token = afw.client.Token("account:read", cli)
```

#### Retrieve all projects in the your Hub
```Python
projs = afw.b360.Project.getProjects(cli, token)

# Print some properties
for p in projs:
    print(p.name)
    print(p.id)
```
### Get project by ID
```Python
proj = afw.b360.Project.getProjectById(cli, token, "PROJECT_ID")
```
### Get all users in the project
```Python
users = afw.b360.Project.getUsersFromProject(token)
```
### Get companies in your hub
```Python
comps = afw.b360.Companies.getCompanies(cli, token)
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

proj = afw.b360.Project.getProjectById(cli, token, "PROJECT_ID")

# Update it, Data is a dictionary with the properties 
# you want to update the template is in the docstring

Data = {
		"name" = "afwExample",
		"status" = "active",
	   }

updatedProject = proj.updateProject(token, Data)

# Updated properties
print(updatedProject.name)
print(updatedProject.status)