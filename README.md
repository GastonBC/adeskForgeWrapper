# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API

As it is right now, it wraps Forge endpoints to make them more friendly to Python. Future releases aim to make common tasks easier, simplifying the steps needed to accomplish things

| | |
|-|-|
|Docs| [https://github.com/GastonBC/adeskForgeWrapper/wiki](https://github.com/GastonBC/adeskForgeWrapper/wiki)
| Full API Reference | [https://gastonbc.github.io/index.html](https://gastonbc.github.io/index.html)

### Setting up credentials and getting a 2 legged token
Notice we will use *cli* and *token* in most methods
```Python
import adeskForgeWrapper as afw
import os

#Your Forge app credentials
forge_client_id = os.getenv('FORGE_CLIENT_ID')
forge_client_secret = os.getenv('FORGE_CLIENT_SECRET')

# Your B360 hub ID and name
bim_account_id = os.getenv('BIM360_ACC_ID')
bim_account_name = os.getenv('BIM360_ACC_NAME')

# We are going to need the token in most methods
cli = afw.client.Client(
	forge_client_id, forge_client_secret, bim_account_id, bim_account_name)

token = afw.client.Token("account:read", cli)
```

#### Retrieve all projects in the your Hub
```Python
projs = afw.b360.Project.get_projects(token)

# Print some properties
for p in projs:
    print(p.name)
    print(p.id)
```
### Get project by ID
```Python
proj = afw.b360.Project.project_by_id(token, "PROJECT_ID")
```
### Get all users in the project
```Python
users = afw.b360.Project.get_users(token)
```
### Get companies in your hub
```Python
comps = afw.b360.Companies.get_companies(token)
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

proj = afw.b360.Project.project_by_id(token, "PROJECT_ID")

# Update it, Data is a dictionary with the properties 
# you want to update the template is in the docstring

Data = {
		"name" = "afwExample",
		"status" = "active",
	   }

updated_project = proj.update_project(token, Data)

# Updated properties
print(updated_project.name)
print(updated_project.status)
