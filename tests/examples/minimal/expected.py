from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class AddressLeaf(BaseModel):
    __root__: str
    """
    Interface IP address. Example value: 10.10.10.1
    """


class PortLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=65535)]
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
    address: AddressLeaf
    """
    Interface IP address. Example value: 10.10.10.1
    """
    port: PortLeaf
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


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid
