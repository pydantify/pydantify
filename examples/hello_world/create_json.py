from pathlib import Path

from endpoint import Model, EndpointContainer, AddressLeaf, PortLeaf

port = PortLeaf(__root__=8080)
host = AddressLeaf(__root__="localhost")

endpoint1 = Model(endpoint=EndpointContainer(address=host, port=port))

json_output = endpoint1.json(indent=2)
with Path("endpoint1.json").open("w") as fp_ep:
    fp_ep.write(json_output)


json_output = endpoint1.json(exclude_defaults=True, by_alias=True, indent=2)
with Path("endpoint1_json_exclude_default_and_by_alias.json").open("w") as fp_ep:
    fp_ep.write(json_output)


endpoint2 = Model(
    endpoint=EndpointContainer(
        address="::1", port=2222, description="Port 2222 on localhost"
    )
)
json_output = endpoint2.json(exclude_defaults=True, by_alias=True, indent=2)
with Path("endpoint2.json").open("w") as fp_ep:
    fp_ep.write(json_output)


endpoint3 = Model(endpoint={"address": "172.0.0.1", "port": 9100})
json_output = endpoint3.json(exclude_defaults=True, by_alias=True, indent=2)
with Path("endpoint3.json").open("w") as fp_ep:
    fp_ep.write(json_output)


endpoint4 = Model(**{"endpoint": {"address": "localhost", "port": 8000}})
json_output = endpoint4.json(exclude_defaults=True, by_alias=True, indent=2)
with Path("endpoint4.json").open("w") as fp_ep:
    fp_ep.write(json_output)
