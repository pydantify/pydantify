from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class UnionLeafLeaf1(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Union_leafLeaf")]
    """
    Number or 'unbounded'
    """


class UnionLeafLeaf(RootModel[Union[UnionLeafLeaf1, str]]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Union[UnionLeafLeaf1, str], Field(title="Union_leafLeaf")]
    """
    Number or 'unbounded'
    """


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    union_leaf: Annotated[UnionLeafLeaf, Field(alias="interfaces:union_leaf")]


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
    interfaces: Annotated[
        InterfacesContainer, Field(None, alias="interfaces:interfaces")
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
