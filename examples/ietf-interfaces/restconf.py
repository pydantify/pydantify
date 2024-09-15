import json
import os

import urllib3
from requests import Session

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
from ietf_interfaces import Model

model = Model.model_validate(response.json())

print(model.model_dump_json(exclude_defaults=True, by_alias=True, indent=2))

print(
    "#" * 17, "Iterate over all interfaces and access name and enable status", "#" * 17
)
for interface in model.interfaces.interface:
    print(
        "Interface {name} is {status}".format(
            name=interface.name.root,
            status="enabled" if interface.enabled.root else "disabled",
        )
    )

print("#" * 17, "Change status and description for the second interface", "#" * 17)
from ietf_interfaces import DescriptionLeaf, EnabledLeaf, InterfacesContainer

interface = model.interfaces.interface[1]
interface.enabled = EnabledLeaf(root=True)
interface.description = DescriptionLeaf(root="https://pydantify.github.io/pydantify/")
print(interface.model_dump_json(exclude_defaults=True, by_alias=True, indent=2))


print("#" * 17, "Create new model only containing second interface", "#" * 17)
new_model = Model(interfaces=InterfacesContainer(interface=[interface]))
print(new_model.model_dump_json(exclude_defaults=True, by_alias=True, indent=2))


print("#" * 17, "Send HTTP patch to update the configuration", "#" * 17)
response = session.patch(
    f"https://{host}/restconf/data/ietf-interfaces:interfaces/",
    data=new_model.model_dump_json(exclude_defaults=True, by_alias=True),
)
response.raise_for_status()


print("#" * 17, "Only send interface to specific interface", "#" * 17)
response = session.patch(
    f"https://{host}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2",
    json={
        "ietf-interfaces:interface": interface.model_dump(
            exclude_defaults=True, by_alias=True
        )
    },
)
response.raise_for_status()
