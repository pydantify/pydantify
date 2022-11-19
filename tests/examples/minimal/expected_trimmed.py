from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel


class AddressLeaf(BaseModel):
    __root__: str
    """
    Interface IP address. Example value: 10.10.10.1
    """


class Model(BaseModel):
    address: AddressLeaf
    """
    Interface IP address. Example value: 10.10.10.1
    """


from pydantic import BaseConfig

BaseConfig.allow_population_by_field_name = True
