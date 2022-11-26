from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel


class AddressLeaf(BaseModel):
    __root__: str
    """
    Target IP address
    """


class PortLeaf(BaseModel):
    __root__: str
    """
    Target port number
    """


class DestinationContainer(BaseModel):
    address: AddressLeaf
    """
    Target IP address
    """
    port: PortLeaf
    """
    Target port number
    """


class PeerContainer(BaseModel):
    destination: DestinationContainer


class InterfacesModule(BaseModel):
    """
    Example demonstrating "uses" keyword
    """

    peer: PeerContainer


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
