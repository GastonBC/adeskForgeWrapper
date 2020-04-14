# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API 

Installation

`pip install adeskForgeWrapper`

Example usage:

```Python
import adeskForgeWrapper as afw
import os

# Your Forge App information
forgeCliId = os.getenv('FORGE_CLIENT_ID')
forgeCliSec = os.getenv('FORGE_CLIENT_SECRET')

# Your BIM 360 account name and id
AccId = os.getenv('BIM360_ACC_ID')
AccName = os.getenv('BIM360_ACC_NAME')

# The client and token will be used in most methods so keep them at hand
cli = afw.client.Client(forgeCliId, forgeCliSec, AccId, AccName)
token = afw.client.Token("account:read", cli)

projs = afw.b360.Project.getProjects(cli, token)

for p in projs:
    print(p.name)
    print(p.id)
```

License
----

MIT
