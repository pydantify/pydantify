from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class AddressLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title='AddressLeaf')]
    """
    Endpoint address. IP or FQDN
    """


class DescriptionLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title='DescriptionLeaf')]
    """
    Endpoint description
    """


class PortType(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=1, le=65535)]


class PortLeaf(RootModel[PortType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[PortType, Field(title='PortLeaf')]
    """
    Port number between 1 and 65535
    """


class EndpointContainer(BaseModel):
    """
    Definition of a endpoint
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    address: Annotated[AddressLeaf, Field(alias='my-endpoint:address')]
    port: Annotated[PortLeaf, Field(alias='my-endpoint:port')]
    description: Annotated[
        DescriptionLeaf, Field(None, alias='my-endpoint:description')
    ]


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
    endpoint: Annotated[EndpointContainer, Field(None, alias='my-endpoint:endpoint')]


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