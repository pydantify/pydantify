from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class DottedQuadType(BaseModel):
    __root__: Annotated[
        str,
        Field(
            regex='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$'
        ),
    ]


class AddressLeaf(BaseModel):
    __root__: DottedQuadType
    """
    Interface IP address. Example value: 10.10.10.1
    """


class SubnetMaskLeaf(BaseModel):
    __root__: DottedQuadType
    """
    Interface subnet mask. Example value: 255.255.255.0
    """


class EnabledLeaf(BaseModel):
    __root__: bool
    """
    Enable or disable the interface. Example value: true
    """


class InterfaceListEntry(BaseModel):
    """
    Regular IPv4 address with subnet
    """

    name: NameLeaf
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    address: AddressLeaf
    """
    Interface IP address. Example value: 10.10.10.1
    """
    subnet_mask: Annotated[SubnetMaskLeaf, Field(alias='subnet-mask')]
    """
    Interface subnet mask. Example value: 255.255.255.0
    """
    enabled: EnabledLeaf = False
    """
    Enable or disable the interface. Example value: true
    """


class InterfacesContainer(BaseModel):
    interface: List[InterfaceListEntry]


class InterfacesModule(BaseModel):
    """
    Example demonstrating typedef statements
    """

    interfaces: InterfacesContainer


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig

BaseConfig.allow_population_by_field_name = True
