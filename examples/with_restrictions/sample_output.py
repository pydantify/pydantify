from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class ComplexAddressLeaf(BaseModel):
    __root__: Annotated[str, Field(regex='^(?=^(\\d{1,3}\\.){3}\\d{1,3}$).*$')]
    """
    Interface IP address. Example value: 10.10.10.1
    """


class ComplexPortLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=65535)]
    """
    Port number. Example value: 8080
    """


class SimplePortLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=65535)]
    """
    Port number. Example value: 8080
    """


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    name: NameLeaf
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    complex_address: Annotated[ComplexAddressLeaf, Field(alias='complex-address')]
    """
    Interface IP address. Example value: 10.10.10.1
    """
    complex_port: Annotated[ComplexPortLeaf, Field(alias='complex-port')]
    """
    Port number. Example value: 8080
    """
    simple_port: Annotated[SimplePortLeaf, Field(alias='simple-port')]
    """
    Port number. Example value: 8080
    """


class InterfacesModule(BaseModel):
    """
    Example using just leafs, containers and modules
    """

    interfaces: InterfacesContainer


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig

BaseConfig.allow_population_by_field_name = True


if __name__ == "__main__":
    # Demonstration purposes only. Not included in actual output.
    # To run: pdm run python out/out.py
    from pathlib import Path

    with open(Path(__file__).parent.joinpath("sample_data.json")) as fd:
        import json

        input = json.load(fd)
        print(f"{input=}")
        model = Model(**input)
        print("Instantiation successful!")

        output = model.json(exclude_defaults=True, by_alias=True)
        print(f"{output=}")

        assert json.loads(output) == input
        print("Serialization successful!")
