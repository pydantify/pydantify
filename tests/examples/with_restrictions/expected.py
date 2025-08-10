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
    complex_address: Annotated[
        str,
        Field(
            alias="interfaces:complex-address",
            pattern="^(?=^(\\d{1,3}\\.){3}\\d{1,3}$).*$",
            title="Complex-addressLeaf",
        ),
    ]
    """
    Interface IP address. Example value: 10.10.10.1
    """
    complex_port: Annotated[
        int,
        Field(
            alias="interfaces:complex-port", ge=1, le=65535, title="Complex-portLeaf"
        ),
    ]
    """
    Port number. Example value: 8080
    """
    simple_port: Annotated[
        int,
        Field(alias="interfaces:simple-port", ge=1, le=65535, title="Simple-portLeaf"),
    ]
    """
    Port number. Example value: 8080
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
    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias="interfaces:interfaces")
    ] = None


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
