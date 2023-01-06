import os
import json
from requests import Session

import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  # for demonstration purposes only

username = os.getenv("RESTCONF_USER", input("Username: "))
password = os.getenv("RESTCONF_PASSWORD", input("Password: "))
host = os.getenv("RESTCONF_HOST", input("Host: "))

session = Session()
session.headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json, application/yang-data.errors+json",
}
session.auth = (username, password)
session.verify = False  # for demonstration purposes only

print("#" * 17, "Get interface data", "#" * 17)
response = session.get(f"https://{host}/restconf/data/ietf-interfaces:interfaces")
response.raise_for_status()
print(json.dumps(response.json(), indent=2))


print("#" * 17, "Convert received data into pydantic model", "#" * 17)
from ietf_interfaces import Model, BaseConfig
from pydantic import Extra

BaseConfig.extra = Extra.ignore
model = Model.parse_obj(response.json())

print(model.json(exclude_defaults=True, by_alias=True, indent=2))

print(
    "#" * 17, "Iterate over all interfaces and access name and enable status", "#" * 17
)
for interface in model.interfaces.interface:
    print(
        "Interface {name} is {status}".format(
            name=interface.name.__root__,
            status="enabled" if interface.enabled.__root__ else "disabled",
        )
    )

print("#" * 17, "Change status and description for the second interface", "#" * 17)
from ietf_interfaces import EnabledLeaf, DescriptionLeaf, InterfacesContainer

interface = model.interfaces.interface[1]
interface.enabled = EnabledLeaf(__root__=True)
interface.description = DescriptionLeaf(
    __root__="https://pydantify.github.io/pydantify/"
)
print(interface.json(exclude_defaults=True, by_alias=True, indent=2))


print("#" * 17, "Create new model only containing second interface", "#" * 17)
new_model = Model(interfaces=InterfacesContainer(interface=[interface]))
print(new_model.json(exclude_defaults=True, by_alias=True, indent=2))


print("#" * 17, "Send HTTP patch to update the configuration", "#" * 17)
response = session.patch(
    f"https://{host}/restconf/data/ietf-interfaces:interfaces/",
    data=new_model.json(exclude_defaults=True, by_alias=True),
)
response.raise_for_status()


print("#" * 17, "Only send interface to specific interface", "#" * 17)
response = session.patch(
    f"https://{host}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2",
    json={
        "ietf-interfaces:interface": interface.dict(
            exclude_defaults=True, by_alias=True
        )
    },
)
response.raise_for_status()
