from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class DestinationContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    address: Annotated[
        Optional[str], Field(alias="interfaces:address", title="AddressLeaf")
    ] = None
    """
    Target IP address
    """
    port: Annotated[Optional[str], Field(alias="interfaces:port", title="PortLeaf")] = (
        None
    )
    """
    Target port number
    """


class PeerContainer(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    destination: Annotated[
        Optional[DestinationContainer], Field(alias="interfaces:destination")
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
    peer: Annotated[Optional[PeerContainer], Field(alias="interfaces:peer")] = None


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
