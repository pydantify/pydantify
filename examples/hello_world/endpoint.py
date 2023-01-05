from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, Field


class AddressLeaf(BaseModel):
    __root__: str
    """
    Endpoint address. IP or FQDN
    """


class PortType(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=65535)]


class PortLeaf(BaseModel):
    __root__: PortType
    """
    Port number between 1 adn 65535
    """


class DescriptionLeaf(BaseModel):
    __root__: str
    """
    Endpoint description
    """


class EndpointContainer(BaseModel):
    """
    Definition of a endpoint
    """

    address: Annotated[AddressLeaf, Field(alias='my-endpoint:address')]
    """
    Endpoint address. IP or FQDN
    """
    port: Annotated[PortLeaf, Field(alias='my-endpoint:port')]
    """
    Port number between 1 adn 65535
    """
    description: Annotated[
        Optional[DescriptionLeaf], Field(alias='my-endpoint:description')
    ] = None
    """
    Endpoint description
    """


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
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    endpoint: Annotated[
        Optional[EndpointContainer], Field(alias='my-endpoint:endpoint')
    ] = None


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True, indent=2)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)