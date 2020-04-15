# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API 

Example usage
Getting all projects in a hub and print it's names and ids

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

# Retrieve all projects in your hub as Project objects
projs = afw.b360.Project.getProjects(cli, token)

# Print names and ids
for p in projs:
    print(p.name)
    print(p.id)
```

License
----

MIT