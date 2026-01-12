from __future__ import annotations

from typing import Annotated, ClassVar, Union

from pydantic import BaseModel, ConfigDict, Field


class Ethernet2Case(BaseModel):
    """
    Option B
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[str] = "if"
    name2: Annotated[str, Field(alias="interfaces:name2")] = None


class EthernetContainer(BaseModel):
    """
    Option A
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[str] = "if"
    name: Annotated[str, Field(alias="interfaces:name")] = None


class EthernetCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[str] = "if"
    ethernet: Annotated[EthernetContainer, Field(alias="interfaces:ethernet")] = None


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
    namespace: ClassVar[str] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[str] = "if"
    interface_type: Annotated[
        Union[EthernetCase, Ethernet2Case],
        Field(alias="interfaces:interface-type"),
    ] = None


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
