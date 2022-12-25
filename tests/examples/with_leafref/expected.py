from __future__ import annotations

from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class TestLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=255)]
    """
    Test node
    """


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name
    """


class IpLeaf(BaseModel):
    __root__: str
    """
    Interface IP
    """


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    test: Annotated[Optional[TestLeaf], Field(alias="interfaces:test")] = None
    """
    Test node
    """
    name: Annotated[Optional[NameLeaf], Field(alias="interfaces:name")] = None
    """
    Interface name
    """
    ip: Annotated[Optional[IpLeaf], Field(alias="interfaces:ip")] = None
    """
    Interface IP
    """


class MgmtInterfaceLeaf(BaseModel):
    __root__: NameLeaf
    """
    Dedicated management interface
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
    - use `exclude_defaults=True` to
    - use `by_alias=True` to ensure qualified names are used ()
    """

    interfaces: Annotated[
        List[InterfacesListEntry], Field(alias="interfaces:interfaces")
    ]
    mgmt_interface: Annotated[
        Optional[MgmtInterfaceLeaf], Field(alias="interfaces:mgmt-interface")
    ] = None
    """
    Dedicated management interface
    """


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
