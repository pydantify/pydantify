from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel


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
    address: AddressLeaf
    """
    Target IP address
    """
    port: PortLeaf
    """
    Target port number
    """


class PeerContainer(BaseModel):
    destination: DestinationContainer


class InterfacesModule(BaseModel):
    """
    Example demonstrating "uses" keyword
    """

    peer: PeerContainer


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True)

    print(f'Generated output: {restconf_payload}')

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
