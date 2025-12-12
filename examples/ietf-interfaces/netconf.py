import os

import ncclient.manager
from ncclient.operations.retrieve import GetReply
from pydantify.utility.xml import model_dump_xml_string, model_validate_xml

username = os.getenv("NETCONF_USER", input("Username: "))
password = os.getenv("NETCONF_PASSWORD", input("Password: "))
host = os.getenv("NETCONF_HOST", input("Host: "))

manager = ncclient.manager.connect(host=host, username=username, password=password)

print("#" * 17, "Get interface data", "#" * 17)
response: GetReply = m.get_config(
    source="running",
    filter=(
        "subtree",
        "<interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'/>",
    ),
)
print(response.xml)


print("#" * 17, "Convert received data into pydantic model", "#" * 17)
from ietf_interfaces import Model

model = model_validate_xml(Model, response.xml)

print(model_dump_xml_string(model, pretty_print=True))

print(
    "#" * 17, "Iterate over all interfaces and access name and enable status", "#" * 17
)
for interface in model.interfaces.interface:
    print(
        "Interface {name} is {status}".format(
            name=interface.name,
            status="enabled" if interface.enabled else "disabled",
        )
    )

print("#" * 17, "Change status and description for the second interface", "#" * 17)
from ietf_interfaces import DescriptionLeaf, EnabledLeaf, InterfacesContainer

interface = model.interfaces.interface[1]
interface.enabled = True
interface.description = "https://pydantify.github.io/pydantify/"
print(model_dump_xml_string(interface, pretty_print=True))


print("#" * 17, "Create new model only containing second interface", "#" * 17)
new_model = Model(interfaces=InterfacesContainer(interface=[interface]))
print(model_dump_xml_string(new_model, pretty_print=True))


print("#" * 17, "Send NETCONF edit-config to update the configuration", "#" * 17)
manager.edit_config(target="running", config=model_dump_xml_string(new_model))


print("#" * 17, "Only send interface to specific interface", "#" * 17)
manager.edit_config(target="running", config=model_dump_xml_string(interface))
