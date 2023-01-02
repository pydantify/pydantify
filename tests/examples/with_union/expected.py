from __future__ import annotations

from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field


class UnionLeafLeafItem(BaseModel):
    __root__: Annotated[int, Field(ge=-2147483648, le=2147483647)]


class UnionLeafLeaf(BaseModel):
    __root__: Union[UnionLeafLeafItem, str]
    """
    Number or 'unbounded'
    """


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    union_leaf: Annotated[UnionLeafLeaf, Field(alias="interfaces:union_leaf")]
    """
    Number or 'unbounded'
    """


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
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias="interfaces:interfaces")
    ] = None


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True, indent=2)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
