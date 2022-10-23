from __future__ import annotations

from typing import List

from pydantic import BaseModel
from pydantic.types import constr


class InterfaceLeaf(BaseModel):
    name: str
    address: constr(
        regex=r'(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
    )
    subnet_mask: str


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
