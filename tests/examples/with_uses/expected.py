from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, Field


class AddressLeaf(BaseModel):
    __root__: str
    """
    Target IP address
    """


class PortLeaf(BaseModel):
    __root__: str
    """
    Target port number
    """


class DestinationContainer(BaseModel):
    address: Annotated[Optional[AddressLeaf], Field(alias="interfaces:address")] = None
    """
    Target IP address
    """
    port: Annotated[Optional[PortLeaf], Field(alias="interfaces:port")] = None
    """
    Target port number
    """


class PeerContainer(BaseModel):
    destination: Annotated[
        Optional[DestinationContainer], Field(alias="interfaces:destination")
    ] = None


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

    peer: Annotated[Optional[PeerContainer], Field(alias="interfaces:peer")] = None


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
