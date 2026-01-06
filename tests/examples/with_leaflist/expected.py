from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field, RootModel


class TaggedLeafList(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=1, le=4094)]
    """
    List of tagged VLANs
    """


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    prefix: str = "if"
    name: Annotated[str, Field(alias="interfaces:name")]
    """
    Interface name
    """
    ip: Annotated[List[str], Field(alias="interfaces:ip")] = []
    """
    List of interface IPs
    """
    tagged: Annotated[
        List[TaggedLeafList], Field(default_factory=list, alias="interfaces:tagged")
    ]
    """
    List of tagged VLANs
    """
    untagged: Annotated[int, Field(alias="interfaces:untagged", ge=1, le=4094)] = None
    """
    Untagged VLAN
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
    namespace: str = "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    prefix: str = "if"
    interfaces: Annotated[
        List[InterfacesListEntry],
        Field(default_factory=list, alias="interfaces:interfaces"),
    ]


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
