from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class DottedQuadType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern="^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$"
        ),
    ]
    """
    Four octets written as decimal numbers and separated with the '.' (full stop) character.
    """


class EnabledLeaf(RootModel[bool]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[bool, Field(title="EnabledLeaf")]
    """
    Enable or disable the interface. Example value: true
    """


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="NameLeaf")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class SubnetMaskLeaf(RootModel[DottedQuadType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[DottedQuadType, Field(title="Subnet-maskLeaf")]
    """
    Interface subnet mask. Example value: 255.255.255.0
    """


class AddressLeaf(RootModel[DottedQuadType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[DottedQuadType, Field(title="AddressLeaf")]
    """
    Interface IP address. Example value: 10.10.10.1
    """


class InterfaceListEntry(BaseModel):
    """
    Regular IPv4 address with subnet
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[NameLeaf, Field(alias="interfaces:name")]
    address: Annotated[AddressLeaf, Field(alias="interfaces:address")]
    subnet_mask: Annotated[SubnetMaskLeaf, Field(alias="interfaces:subnet-mask")]
    enabled: Annotated[EnabledLeaf, Field(False, alias="interfaces:enabled")]


class InterfacesContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    interface: Annotated[List[InterfaceListEntry], Field(alias="interfaces:interface")]


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
