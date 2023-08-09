from __future__ import annotations

from typing import Annotated, Any, List, Optional

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


class TpidLeaf(BaseModel):
    __root__: Any
    """
    Optionally set the tag protocol identifier field (TPID) that
    is accepted on the VLAN
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
    tpid: Annotated[TpidLeaf, Field(alias="interfaces:tpid")] = "TPID_0X8100"
    """
    Optionally set the tag protocol identifier field (TPID) that
    is accepted on the VLAN
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
