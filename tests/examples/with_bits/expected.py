from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    name: Annotated[str, Field(alias="interfaces:name", title="NameLeaf")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    mybits: Annotated[
        Optional[str],
        Field(
            alias="interfaces:mybits",
            pattern="^(disable-nagle|auto-sense-speed|ten-mb-only|\\s)*$",
            title="MybitsLeaf",
        ),
    ] = None


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
    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias="interfaces:interfaces")
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
