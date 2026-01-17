from __future__ import annotations

from typing import Annotated, ClassVar, List

from pydantic import BaseModel, ConfigDict, Field, RootModel


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    namespace: ClassVar[str] = "configuration"
    name: Annotated[str, Field(alias="configuration:name")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    ip: Annotated[str, Field(alias="configuration:ip")] = None
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
    namespace: ClassVar[str] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    namespace: ClassVar[str] = "configuration"
    name: Annotated[str, Field(alias="configuration:name")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    interfaces: Annotated[
        List[InterfacesListEntry],
        Field(default_factory=list, alias="configuration:interfaces"),
    ]


class ConfigurationContainer(BaseModel):
    """
    Just a simple example of a container with uses.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    namespace: ClassVar[str] = "configuration"
    devicename: Annotated[str, Field(alias="configuration:devicename")]
    """
    Device name. Example value: sw01
    """
    namespaces: Annotated[
        List[NamespacesListEntry],
        Field(default_factory=list, alias="configuration:namespaces"),
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
        regex_engine="python-re",
    )
    namespace: ClassVar[str] = (
        "http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration"
    )
    namespace: ClassVar[str] = "configuration"
    configuration: Annotated[
        ConfigurationContainer, Field(alias="configuration:configuration")
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
