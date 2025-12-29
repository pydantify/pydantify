from __future__ import annotations

from typing import Annotated, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class UnionLeafLeaf1(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=-2147483648, le=2147483647)]
    """
    Number or 'unbounded'
    """


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: Optional[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: Optional[str] = "if"
    union_leaf: Annotated[
        Union[UnionLeafLeaf1, str], Field(alias="interfaces:union_leaf")
    ]
    """
    Number or 'unbounded'
    """


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
        regex_engine="python-re",
    )
    namespace: Optional[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: Optional[str] = "if"
    interfaces: Annotated[InterfacesContainer, Field(alias="interfaces:interfaces")] = (
        None
    )


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
