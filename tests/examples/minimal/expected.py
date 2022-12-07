from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """


class AddressLeaf(BaseModel):
    __root__: str
    """
    Interface IP address. Example value: 10.10.10.1
    """


class PortLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=65535)]
    """
    Port number. Example value: 8080
    """


class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    name: Annotated[NameLeaf, Field(alias='interfaces:name')]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    address: Annotated[AddressLeaf, Field(alias='interfaces:address')]
    """
    Interface IP address. Example value: 10.10.10.1
    """
    port: Annotated[PortLeaf, Field(alias='interfaces:port')]
    """
    Port number. Example value: 8080
    """


class InterfacesModule(BaseModel):
    """
    Example using just leafs, containers and modules
    """

    interfaces: InterfacesContainer


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
