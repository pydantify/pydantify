from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import constr


class DottedQuadType(
    constr(
        regex=r'(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
    )
):
    """Four octets written as decimal numbers and separated with the '.' (full stop) character."""


class InterfaceLeaf(BaseModel):
    name: Annotated[str, Field(description="Interface name. Example value: GigabitEthernet 0/0/0")]
    address: Annotated[
        DottedQuadType,
        Field(description="Interface IP address. Example value: 10.10.10.1"),
    ]
    subnet_mask: Annotated[str, Field(description="Interface subnet mask. Example value: 255.255.255.0")]
    enabled: bool = Field(False, description="Enable or disable the interface. Example value: true")


class InterfaceList(List[InterfaceLeaf]):
    pass


class InterfaceContainer(BaseModel):
    interface: InterfaceList


class InterfacesModule(BaseModel):
    interfaces: InterfaceContainer


# Demonstration purposes only. Not included in actual output.
if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent.joinpath("sample_data.json")) as fd:
        import json

        data = json.load(fd)
        a = InterfacesModule(**data)
        print("Instantiation successful!")
        print(f"Output: {a.json()}")
        assert json.loads(a.json()) == data
        print("Serialization successful!")
