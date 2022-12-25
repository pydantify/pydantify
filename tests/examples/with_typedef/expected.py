from __future__ import annotations

from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class DottedQuadType(BaseModel):
    __root__: Annotated[
        str,
        Field(
            regex="^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$"
        ),
    ]
    """
    Four octets written as decimal numbers and separated with the '.' (full stop) character.
    """


class AddressLeaf(BaseModel):
    __root__: DottedQuadType
    """
    Interface IP address. Example value: 10.10.10.1
    """


class SubnetMaskLeaf(BaseModel):
    __root__: DottedQuadType
    """
    Interface subnet mask. Example value: 255.255.255.0
    """


class EnabledLeaf(BaseModel):
    __root__: bool
    """
    Enable or disable the interface. Example value: true
    """


class InterfaceListEntry(BaseModel):
    """
    Regular IPv4 address with subnet
    """

    name: Annotated[NameLeaf, Field(alias="interfaces:name")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    address: Annotated[AddressLeaf, Field(alias="interfaces:address")]
    """
    Interface IP address. Example value: 10.10.10.1
    """
    subnet_mask: Annotated[SubnetMaskLeaf, Field(alias="interfaces:subnet-mask")]
    """
    Interface subnet mask. Example value: 255.255.255.0
    """
    enabled: Annotated[EnabledLeaf, Field(alias="interfaces:enabled")] = False
    """
    Enable or disable the interface. Example value: true
    """


class InterfacesContainer(BaseModel):
    interface: Annotated[List[InterfaceListEntry], Field(alias="interfaces:interface")]


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

    restconf_payload = model.json(exclude_defaults=True, by_alias=True)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
