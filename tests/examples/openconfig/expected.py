from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class DescriptionLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="DescriptionLeaf")]
    """
    A textual description of the interface.

    A server implementation MAY map this leaf to the ifAlias
    MIB object.  Such an implementation needs to use some
    mechanism to handle the differences in size and characters
    allowed between this leaf and ifAlias.  The definition of
    such a mechanism is outside the scope of this document.

    Since ifAlias is defined to be stored in non-volatile
    storage, the MIB implementation MUST map ifAlias to the
    value of 'description' in the persistently stored
    datastore.

    Specifically, if the device supports ':startup', when
    ifAlias is read the device MUST return the value of
    'description' in the 'startup' datastore, and when it is
    written, it MUST be written to the 'running' and 'startup'
    datastores.  Note that it is up to the implementation to

    decide whether to modify this single leaf in 'startup' or
    perform an implicit copy-config from 'running' to
    'startup'.

    If the device does not support ':startup', ifAlias MUST
    be mapped to the 'description' leaf in the 'running'
    datastore.
    """


class EnabledLeaf(RootModel[bool]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[bool, Field(title="EnabledLeaf")]
    """
    This leaf contains the configured, desired state of the
    interface.

    Systems that implement the IF-MIB use the value of this
    leaf in the 'running' datastore to set
    IF-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry
    has been initialized, as described in RFC 2863.

    Changes in this leaf in the 'running' datastore are
    reflected in ifAdminStatus, but if ifAdminStatus is
    changed over SNMP, this leaf is not affected.
    """


class LoopbackModeLeaf(RootModel[bool]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[bool, Field(title="Loopback-modeLeaf")]
    """
    When set to true, the interface is logically looped back,
    such that packets that are forwarded via the interface
    are received on the same interface.
    """


class MtuLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=65535, title="MtuLeaf")]
    """
    Set the max transmission unit size in octets
    for the physical interface.  If this is not set, the mtu is
    set to the operational default -- e.g., 1514 bytes on an
    Ethernet interface.
    """


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="NameLeaf")]
    """
    The name of the interface.

    A device MAY restrict the allowed values for this leaf,
    possibly depending on the type of the interface.
    For system-controlled interfaces, this leaf is the
    device-specific name of the interface.  The 'config false'
    list interfaces/interface[name]/state contains the currently
    existing interfaces on the device.

    If a client tries to create configuration for a
    system-controlled interface that is not present in the
    corresponding state list, the server MAY reject
    the request if the implementation does not support
    pre-provisioning of interfaces or if the name refers to
    an interface that can never exist in the system.  A
    NETCONF server MUST reply with an rpc-error with the
    error-tag 'invalid-value' in this case.

    The IETF model in RFC 7223 provides YANG features for the
    following (i.e., pre-provisioning and arbitrary-names),
    however they are omitted here:

     If the device supports pre-provisioning of interface
     configuration, the 'pre-provisioning' feature is
     advertised.

     If the device allows arbitrarily named user-controlled
     interfaces, the 'arbitrary-names' feature is advertised.

    When a configured user-controlled interface is created by
    the system, it is instantiated with the same name in the
    /interfaces/interface[name]/state list.
    """


class TypeLeaf(RootModel[Any]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Any, Field(title="TypeLeaf")]
    """
    The type of the interface.

    When an interface entry is created, a server MAY
    initialize the type leaf with a valid value, e.g., if it
    is possible to derive the type from the name of the
    interface.

    If a client tries to set the type of an interface to a
    value that can never be used by the system, e.g., if the
    type is not supported or if the type does not match the
    name of the interface, the server MUST reject the request.
    A NETCONF server MUST reply with an rpc-error with the
    error-tag 'invalid-value' in this case.
    """


class ConfigContainer(BaseModel):
    """
    Configurable items at the global, physical interface
    level
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[NameLeaf, Field(None, alias="openconfig-interfaces:name")]
    type: Annotated[TypeLeaf, Field(alias="openconfig-interfaces:type")]
    mtu: Annotated[MtuLeaf, Field(None, alias="openconfig-interfaces:mtu")]
    loopback_mode: Annotated[
        LoopbackModeLeaf, Field(False, alias="openconfig-interfaces:loopback-mode")
    ]
    description: Annotated[
        DescriptionLeaf, Field(None, alias="openconfig-interfaces:description")
    ]
    enabled: Annotated[EnabledLeaf, Field(True, alias="openconfig-interfaces:enabled")]


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
    config: Annotated[
        ConfigContainer, Field(None, alias="openconfig-interfaces:config")
    ]


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
