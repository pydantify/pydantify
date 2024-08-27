from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class Name2Leaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="Name2Leaf")]


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="NameLeaf")]


class Ethernet2Case(BaseModel):
    """
    Option B
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name2: Annotated[Name2Leaf, Field(None, alias="interfaces:name2")]


class EthernetContainer(BaseModel):
    """
    Option A
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[NameLeaf, Field(None, alias="interfaces:name")]


class EthernetCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ethernet: Annotated[EthernetContainer, Field(None, alias="interfaces:ethernet")]


class Model(BaseModel):
    """
    Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

    ## Tips
    Initialization:
    - all values have to be set via keyword arguments
    - if a class contains only a `root` field, it can be initialized as follows:
        - `member=MyNode(root=<value>)`
        - `member=<value>`

    Serialziation:
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    interface_type: Annotated[
        Union[EthernetCase, Ethernet2Case],
        Field(None, alias="interfaces:interface-type"),
    ]


if __name__ == "__main__":
    model = Model(  # type: ignore[call-arg]
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
