from __future__ import annotations

from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name
    """


class IpLeafList(BaseModel):
    __root__: str
    """
    List of interface IPs
    """


class VlanIdType(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=4094)]


class TaggedLeafList(BaseModel):
    __root__: VlanIdType
    """
    List of tagged VLANs
    """


class UntaggedLeaf(BaseModel):
    __root__: VlanIdType
    """
    Untagged VLAN
    """


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    name: Annotated[Optional[NameLeaf], Field(alias="interfaces:name")] = None
    """
    Interface name
    """
    ip: Annotated[List[IpLeafList], Field(alias="interfaces:ip")] = []
    """
    List of interface IPs
    """
    tagged: Annotated[List[TaggedLeafList], Field(alias="interfaces:tagged")] = []
    """
    List of tagged VLANs
    """
    untagged: Annotated[
        Optional[UntaggedLeaf], Field(alias="interfaces:untagged")
    ] = None
    """
    Untagged VLAN
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
        List[InterfacesListEntry], Field(alias="interfaces:interfaces")
    ]


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
