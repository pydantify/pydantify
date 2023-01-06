from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, List, Optional

from pydantic import BaseModel, Field


class NameLeaf(BaseModel):
    __root__: str
    """
    The name of the interface.

    A device MAY restrict the allowed values for this leaf,
    possibly depending on the type of the interface.
    For system-controlled interfaces, this leaf is the
    device-specific name of the interface.  The 'config false'
    list /interfaces-state/interface contains the currently
    existing interfaces on the device.

    If a client tries to create configuration for a
    system-controlled interface that is not present in the
    /interfaces-state/interface list, the server MAY reject
    the request if the implementation does not support
    pre-provisioning of interfaces or if the name refers to
    an interface that can never exist in the system.  A
    NETCONF server MUST reply with an rpc-error with the
    error-tag 'invalid-value' in this case.

    If the device supports pre-provisioning of interface
    configuration, the 'pre-provisioning' feature is
    advertised.

    If the device allows arbitrarily named user-controlled
    interfaces, the 'arbitrary-names' feature is advertised.

    When a configured user-controlled interface is created by
    the system, it is instantiated with the same name in the
    /interface-state/interface list.
    """


class DescriptionLeaf(BaseModel):
    __root__: str
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


class TypeLeaf(BaseModel):
    __root__: Any
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


class EnabledLeaf(BaseModel):
    __root__: bool
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


class EnumerationEnum(Enum):
    """
    An enumeration.
    """

    int_1 = 1
    int_2 = 2


class LinkUpDownTrapEnableLeaf(BaseModel):
    __root__: EnumerationEnum
    """
    Controls whether linkUp/linkDown SNMP notifications
    should be generated for this interface.

    If this node is not configured, the value 'enabled' is
    operationally used by the server for interfaces that do
    not operate on top of any other interface (i.e., there are
    no 'lower-layer-if' entries), and 'disabled' otherwise.
    """


class InterfaceListEntry(BaseModel):
    """
    The list of configured interfaces on the device.

    The operational state of an interface is available in the
    /interfaces-state/interface list.  If the configuration of a
    system-controlled interface cannot be used by the system
    (e.g., the interface hardware present does not match the
    interface type), then the configuration is not applied to
    the system-controlled interface shown in the
    /interfaces-state/interface list.  If the configuration
    of a user-controlled interface cannot be used by the system,
    the configured interface is not instantiated in the
    /interfaces-state/interface list.
    """

    name: Annotated[Optional[NameLeaf], Field(alias="ietf-interfaces:name")] = None
    """
    The name of the interface.

    A device MAY restrict the allowed values for this leaf,
    possibly depending on the type of the interface.
    For system-controlled interfaces, this leaf is the
    device-specific name of the interface.  The 'config false'
    list /interfaces-state/interface contains the currently
    existing interfaces on the device.

    If a client tries to create configuration for a
    system-controlled interface that is not present in the
    /interfaces-state/interface list, the server MAY reject
    the request if the implementation does not support
    pre-provisioning of interfaces or if the name refers to
    an interface that can never exist in the system.  A
    NETCONF server MUST reply with an rpc-error with the
    error-tag 'invalid-value' in this case.

    If the device supports pre-provisioning of interface
    configuration, the 'pre-provisioning' feature is
    advertised.

    If the device allows arbitrarily named user-controlled
    interfaces, the 'arbitrary-names' feature is advertised.

    When a configured user-controlled interface is created by
    the system, it is instantiated with the same name in the
    /interface-state/interface list.
    """
    description: Annotated[
        Optional[DescriptionLeaf], Field(alias="ietf-interfaces:description")
    ] = None
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
    type: Annotated[TypeLeaf, Field(alias="ietf-interfaces:type")]
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
    enabled: Annotated[EnabledLeaf, Field(alias="ietf-interfaces:enabled")] = True
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
    link_up_down_trap_enable: Annotated[
        Optional[LinkUpDownTrapEnableLeaf],
        Field(alias="ietf-interfaces:link-up-down-trap-enable"),
    ] = None
    """
    Controls whether linkUp/linkDown SNMP notifications
    should be generated for this interface.

    If this node is not configured, the value 'enabled' is
    operationally used by the server for interfaces that do
    not operate on top of any other interface (i.e., there are
    no 'lower-layer-if' entries), and 'disabled' otherwise.
    """


class InterfacesContainer(BaseModel):
    """
    Interface configuration parameters.
    """

    interface: Annotated[
        List[InterfaceListEntry], Field(alias="ietf-interfaces:interface")
    ]


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

    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias="ietf-interfaces:interfaces")
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
