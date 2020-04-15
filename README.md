# adeskForgeWrapper - afw

afw is a simple Python wrapper for Autodesk's Forge API 

Example usage
Getting all projects in a hub and print it's names and ids

```Python
import adeskForgeWrapper as afw
import os

forgeCliId = os.getenv('FORGE_CLIENT_ID')
forgeCliSec = os.getenv('FORGE_CLIENT_SECRET')

AccId = os.getenv('BIM360_ACC_ID')
AccName = os.getenv('BIM360_ACC_NAME')


cli = afw.client.Client(forgeCliId, forgeCliSec, fairyB360AccId,fairyB360AccName)
token = afw.client.Token("account:read", cli)

projs = afw.b360.Project.getProjects(cli, token)

for p in projs:
    print(p.name)
    print(p.id)
```

License
----

MIT
