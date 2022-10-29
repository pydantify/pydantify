from __future__ import annotations

from pydantic import BaseModel


class AddressLeaf(str):
    """Interface name. Example value: GigabitEthernet 0/0/0"""


class InterfacesModule(BaseModel):
    address: AddressLeaf


# Demonstration purposes only. Not included in actual output.
# To run: pdm run python examples/minimal/sample_output.py
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
