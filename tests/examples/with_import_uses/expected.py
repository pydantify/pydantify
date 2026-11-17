from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    prefix: ClassVar[str | None] = "configuration"
    name: Annotated[
        str,
        Field(
            serialization_alias="configuration:name",
            validation_alias=AliasChoices("configuration:name", "name"),
        ),
    ]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    ip: Annotated[
        str | None,
        Field(
            serialization_alias="configuration:ip",
            validation_alias=AliasChoices("configuration:ip", "ip"),
        ),
    ] = None
    """
    Interface IP
    """


class NamespacesListEntry(BaseModel):
    """
    List of configured device namespaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    prefix: ClassVar[str | None] = "configuration"
    name: Annotated[
        str,
        Field(
            serialization_alias="configuration:name",
            validation_alias=AliasChoices("configuration:name", "name"),
        ),
    ]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    interfaces: Annotated[
        list[InterfacesListEntry] | None,
        Field(
            serialization_alias="configuration:interfaces",
            validate_default=True,
            validation_alias=AliasChoices("configuration:interfaces", "interfaces"),
        ),
    ] = []


class ConfigurationContainer(BaseModel):
    """
    Just a simple example of a container with uses.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    prefix: ClassVar[str | None] = "configuration"
    devicename: Annotated[
        str,
        Field(
            serialization_alias="configuration:devicename",
            validation_alias=AliasChoices("configuration:devicename", "devicename"),
        ),
    ]
    """
    Device name. Example value: sw01
    """
    namespaces: Annotated[
        list[NamespacesListEntry] | None,
        Field(
            serialization_alias="configuration:namespaces",
            validate_default=True,
            validation_alias=AliasChoices("configuration:namespaces", "namespaces"),
        ),
    ] = []


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
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    prefix: ClassVar[str | None] = "configuration"
    configuration: Annotated[
        ConfigurationContainer | None,
        Field(
            serialization_alias="configuration:configuration",
            validation_alias=AliasChoices(
                "configuration:configuration", "configuration"
            ),
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
