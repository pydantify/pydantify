from __future__ import annotations

from typing import Annotated, ClassVar, List

from pydantic import BaseModel, ConfigDict, Field, RootModel


class DottedQuadType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$'
        ),
    ]
    """
    Four octets written as decimal numbers and separated with the '.' (full stop) character.
    """


class EnabledLeaf(RootModel[bool]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: bool
    """
    Enable or disable the interface. Example value: true
    """


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class SubnetMaskLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$'
        ),
    ]
    """
    Interface subnet mask. Example value: 255.255.255.0
    """


class AddressLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$'
        ),
    ]
    """
    Interface IP address. Example value: 10.10.10.1
    """


class InterfaceListEntry(BaseModel):
    """
    Regular IPv4 address with subnet
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces'
    prefix: ClassVar = 'if'
    name: Annotated[str, Field(alias='interfaces:name')]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    address: Annotated[
        str,
        Field(
            alias='interfaces:address',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$',
        ),
    ]
    """
    Interface IP address. Example value: 10.10.10.1
    """
    subnet_mask: Annotated[
        str,
        Field(
            alias='interfaces:subnet-mask',
            pattern='^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$',
        ),
    ]
    """
    Interface subnet mask. Example value: 255.255.255.0
    """
    enabled: Annotated[bool, Field(alias='interfaces:enabled')] = False
    """
    Enable or disable the interface. Example value: true
    """


class InterfacesContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces'
    prefix: ClassVar = 'if'
    interface: Annotated[
        List[InterfaceListEntry],
        Field(default_factory=list, alias='interfaces:interface'),
    ]


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
    namespace: ClassVar = 'http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces'
    prefix: ClassVar = 'if'
    interfaces: Annotated[InterfacesContainer, Field(alias='interfaces:interfaces')] = (
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