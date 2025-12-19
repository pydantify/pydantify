from pathlib import Path
from endpoint import Model, EndpointContainer
from pydantify.utility.netconf import model_dump_xml_string

port = 8080
host = "localhost"

endpoint1 = Model(endpoint=EndpointContainer(address=host, port=port))
xml_output = model_dump_xml_string(endpoint1, pretty_print=True)
with Path("endpoint1.xml").open("w") as fp_ep:
    fp_ep.write(xml_output)


endpoint2 = Model(
    endpoint=EndpointContainer(
        address="::1", port=2222, description="Port 2222 on localhost"
    )
)
xml_output2 = model_dump_xml_string(endpoint2, pretty_print=True)
with Path("endpoint2.xml").open("w") as fp:
    fp.write(xml_output2)


endpoint3 = Model(endpoint={"address": "172.0.0.1", "port": 9100})
xml_output = model_dump_xml_string(endpoint3, pretty_print=True)
with Path("endpoint3.xml").open("w") as fp_ep:
    fp_ep.write(xml_output)


endpoint4 = Model(
    **{"endpoint": {"my-endpoint:address": "localhost", "my-endpoint:port": 8000}}
)
xml_output = model_dump_xml_string(endpoint4, pretty_print=True)
with Path("endpoint4.xml").open("w") as fp_ep:
    fp_ep.write(xml_output)

endpoint5 = Model.model_validate(
    {
        "my-endpoint:endpoint": {
            "my-endpoint:address": "remote",
            "my-endpoint:port": 53,
        }
    }
)
xml_output = model_dump_xml_string(endpoint5, pretty_print=True)
with Path("endpoint5.xml").open("w") as fp_ep:
    fp_ep.write(xml_output)
