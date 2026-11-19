from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class EndpointContainer(BaseModel):
    """
    Definition of a endpoint
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = (
        "http://pydantify.github.io/ns/yang/pydantify-endpoint"
    )
    prefix: ClassVar[str | None] = "ep"
    address: Annotated[
        str,
        Field(
            serialization_alias="my-endpoint:address",
            validation_alias=AliasChoices("my-endpoint:address", "address"),
        ),
    ]
    """
    Endpoint address. IP or FQDN
    """
    port: Annotated[
        int,
        Field(
            ge=1,
            le=65535,
            serialization_alias="my-endpoint:port",
            validation_alias=AliasChoices("my-endpoint:port", "port"),
        ),
    ]
    """
    Port number between 1 and 65535
    """
    description: Annotated[
        str | None,
        Field(
            serialization_alias="my-endpoint:description",
            validation_alias=AliasChoices("my-endpoint:description", "description"),
        ),
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
    namespace: ClassVar[str | None] = (
        "http://pydantify.github.io/ns/yang/pydantify-endpoint"
    )
    prefix: ClassVar[str | None] = "ep"
    endpoint: Annotated[
        EndpointContainer | None,
        Field(
            serialization_alias="my-endpoint:endpoint",
            validation_alias=AliasChoices("my-endpoint:endpoint", "endpoint"),
        ),
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
