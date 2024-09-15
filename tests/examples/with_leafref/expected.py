from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class IpLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="IpLeaf")]
    """
    Interface IP
    """


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: str
    """
    Interface name
    """


class TestLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=255, title="TestLeaf")]
    """
    Test node
    """


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    test: Annotated[TestLeaf, Field(None, alias="interfaces:test")]
    name: Annotated[NameLeaf, Field(None, alias="interfaces:name")]
    ip: Annotated[IpLeaf, Field(None, alias="interfaces:ip")]


class MgmtInterfaceLeaf(RootModel[NameLeaf]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[NameLeaf, Field(title="Mgmt-interfaceLeaf")]
    """
    Dedicated management interface
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
    )
    interfaces: Annotated[
        List[InterfacesListEntry], Field(alias="interfaces:interfaces")
    ]
    mgmt_interface: Annotated[
        MgmtInterfaceLeaf, Field(None, alias="interfaces:mgmt-interface")
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
