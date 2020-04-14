# adeskForgeWrapper - afw


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

afw is a simple Python wrapper for Autodesk's Forge API 

Example usage:

```Python
import adeskForgeWrapper as afw
import os

forgeCliId = os.getenv('FORGE_CLIENT_ID')
forgeCliSec = os.getenv('FORGE_CLIENT_SECRET')

AccId = os.getenv('BIM360_ACC_ID')
AccName = os.getenv('BIM360_ACC_NAME')


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
