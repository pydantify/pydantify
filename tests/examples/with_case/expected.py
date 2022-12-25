from __future__ import annotations

from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str


class EthernetContainer(BaseModel):
    """
    Option A
    """

    name: Annotated[Optional[NameLeaf], Field(alias="interfaces:name")] = None


class EthernetCase(BaseModel):
    ethernet: Annotated[
        Optional[EthernetContainer], Field(alias="interfaces:ethernet")
    ] = None


class Name2Leaf(BaseModel):
    __root__: str


class Ethernet2Case(BaseModel):
    """
    Option B
    """

    name2: Annotated[Optional[Name2Leaf], Field(alias="interfaces:name2")] = None


class Model(BaseModel):
    """
    Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

    ## Tips
    Initialization:
    - all values have to be set via keyword arguments
    - if a class contains only a `__root__` field, it can be initialized as follows:
        - `member=MyNode(__root__=<value>)`
        - `member=<value>`

    Serialziation:
    - use `exclude_defaults=True` to
    - use `by_alias=True` to ensure qualified names are used ()
    """

    interface_type: Annotated[
        Optional[Union[EthernetCase, Ethernet2Case]],
        Field(alias="interfaces:interface-type"),
    ] = None


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
