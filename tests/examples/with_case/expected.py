from __future__ import annotations

from typing import Annotated, Union

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str


class EthernetContainer(BaseModel):
    """
    Option A
    """

    name: NameLeaf


class EthernetCase(BaseModel):
    ethernet: EthernetContainer


class Name2Leaf(BaseModel):
    __root__: str


class Ethernet2Case(BaseModel):
    """
    Option B
    """

    name2: Name2Leaf


class InterfacesModule(BaseModel):
    """
    Example demonstarating leafref nodes
    """

    interface_type: Annotated[Union[EthernetCase, Ethernet2Case], Field(alias='interface-type')]


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid
