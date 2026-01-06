from __future__ import annotations

from enum import Enum
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field, RootModel


class EnumerationEnum(Enum):
    up = "UP"
    down = "DOWN"
    testing = "TESTING"


class EnumerationEnum2(Enum):
    up = "UP"
    down = "DOWN"
    testing = "TESTING"
    unknown = "UNKNOWN"
    dormant = "DORMANT"
    not_present = "NOT_PRESENT"
    lower_layer_down = "LOWER_LAYER_DOWN"


class EnumerationEnum3(Enum):
    up = "UP"
    down = "DOWN"
    testing = "TESTING"


class EnumerationEnum4(Enum):
    up = "UP"
    down = "DOWN"
    testing = "TESTING"
    unknown = "UNKNOWN"
    dormant = "DORMANT"
    not_present = "NOT_PRESENT"
    lower_layer_down = "LOWER_LAYER_DOWN"


class AdminStatusLeaf(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum
    """
    The desired state of the interface.  In RFC 7223 this leaf
    has the same read semantics as ifAdminStatus.  Here, it
    reflects the administrative state as set by enabling or
    disabling the interface.
    """


class AdminStatusLeaf2(RootModel[EnumerationEnum3]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum3
    """
    The desired state of the interface.  In RFC 7223 this leaf
    has the same read semantics as ifAdminStatus.  Here, it
    reflects the administrative state as set by enabling or
    disabling the interface.
    """


class OperStatusLeaf(RootModel[EnumerationEnum2]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum2
    """
    The current operational state of the interface.

    This leaf has the same semantics as ifOperStatus.
    """


class OperStatusLeaf2(RootModel[EnumerationEnum4]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum4
    """
    The current operational state of the interface.

    This leaf has the same semantics as ifOperStatus.
    """


class StateContainer2(BaseModel):
    """
    Operational state data for interface hold-time.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    up: Annotated[int, Field(alias="openconfig-interfaces:up", ge=0, le=4294967295)] = 0
    """
    Dampens advertisement when the interface
    transitions from down to up.  A zero value means dampening
    is turned off, i.e., immediate notification.
    """
    down: Annotated[
        int, Field(alias="openconfig-interfaces:down", ge=0, le=4294967295)
    ] = 0
    """
    Dampens advertisement when the interface transitions from
    up to down.  A zero value means dampening is turned off,
    i.e., immediate notification.
    """


class CountersContainer(BaseModel):
    """
    A collection of interface-related statistics objects.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    in_octets: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-octets", ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets received on the interface,
    including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_unicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-unicast-pkts", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were not addressed to a
    multicast or broadcast address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_broadcast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-broadcast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a broadcast
    address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_multicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-multicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a multicast
    address at this sub-layer.  For a MAC-layer protocol,
    this includes both Group and Functional addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_discards: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-discards", ge=0, le=18446744073709551615),
    ] = None
    """
    The number of inbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being deliverable to a higher-layer
    protocol.  One possible reason for discarding such a
    packet could be to free up buffer space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_errors: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-errors", ge=0, le=18446744073709551615),
    ] = None
    """
    For packet-oriented interfaces, the number of inbound
    packets that contained errors preventing them from being
    deliverable to a higher-layer protocol.  For character-
    oriented or fixed-length interfaces, the number of
    inbound transmission units that contained errors
    preventing them from being deliverable to a higher-layer
    protocol.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_unknown_protos: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-unknown-protos",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    For packet-oriented interfaces, the number of packets
    received via the interface that were discarded because
    of an unknown or unsupported protocol.  For
    character-oriented or fixed-length interfaces that
    support protocol multiplexing, the number of
    transmission units received via the interface that were
    discarded because of an unknown or unsupported protocol.
    For any interface that does not support protocol
    multiplexing, this counter is not present.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_fcs_errors: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-fcs-errors", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    Number of received packets which had errors in the
    frame check sequence (FCS), i.e., framing errors.

    Discontinuities in the value of this counter can occur
    when the device is re-initialization as indicated by the
    value of 'last-clear'.
    """
    out_octets: Annotated[
        int,
        Field(alias="openconfig-interfaces:out-octets", ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets transmitted out of the
    interface, including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_unicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-unicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were not addressed
    to a multicast or broadcast address at this sub-layer,
    including those that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_broadcast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-broadcast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were addressed to a
    broadcast address at this sub-layer, including those
    that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_multicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-multicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were addressed to a
    multicast address at this sub-layer, including those
    that were discarded or not sent.  For a MAC-layer
    protocol, this includes both Group and Functional
    addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_discards: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-discards", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The number of outbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being transmitted.  One possible reason
    for discarding such a packet could be to free up buffer
    space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_errors: Annotated[
        int,
        Field(alias="openconfig-interfaces:out-errors", ge=0, le=18446744073709551615),
    ] = None
    """
    For packet-oriented interfaces, the number of outbound
    packets that could not be transmitted because of errors.
    For character-oriented or fixed-length interfaces, the
    number of outbound transmission units that could not be
    transmitted because of errors.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    carrier_transitions: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:carrier-transitions",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    Number of times the interface state has transitioned
    between up and down since the time the device restarted
    or the last-clear time, whichever is most recent.
    """
    last_clear: Annotated[
        int,
        Field(alias="openconfig-interfaces:last-clear", ge=0, le=18446744073709551615),
    ] = None
    """
    Timestamp of the last time the interface counters were
    cleared.

    The value is the timestamp in nanoseconds relative to
    the Unix Epoch (Jan 1, 1970 00:00:00 UTC).
    """


class CountersContainer2(BaseModel):
    """
    A collection of interface-related statistics objects.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    in_octets: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-octets", ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets received on the interface,
    including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_unicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-unicast-pkts", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were not addressed to a
    multicast or broadcast address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_broadcast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-broadcast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a broadcast
    address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_multicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-multicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a multicast
    address at this sub-layer.  For a MAC-layer protocol,
    this includes both Group and Functional addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_discards: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-discards", ge=0, le=18446744073709551615),
    ] = None
    """
    The number of inbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being deliverable to a higher-layer
    protocol.  One possible reason for discarding such a
    packet could be to free up buffer space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_errors: Annotated[
        int,
        Field(alias="openconfig-interfaces:in-errors", ge=0, le=18446744073709551615),
    ] = None
    """
    For packet-oriented interfaces, the number of inbound
    packets that contained errors preventing them from being
    deliverable to a higher-layer protocol.  For character-
    oriented or fixed-length interfaces, the number of
    inbound transmission units that contained errors
    preventing them from being deliverable to a higher-layer
    protocol.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_unknown_protos: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-unknown-protos",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    For packet-oriented interfaces, the number of packets
    received via the interface that were discarded because
    of an unknown or unsupported protocol.  For
    character-oriented or fixed-length interfaces that
    support protocol multiplexing, the number of
    transmission units received via the interface that were
    discarded because of an unknown or unsupported protocol.
    For any interface that does not support protocol
    multiplexing, this counter is not present.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    in_fcs_errors: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:in-fcs-errors", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    Number of received packets which had errors in the
    frame check sequence (FCS), i.e., framing errors.

    Discontinuities in the value of this counter can occur
    when the device is re-initialization as indicated by the
    value of 'last-clear'.
    """
    out_octets: Annotated[
        int,
        Field(alias="openconfig-interfaces:out-octets", ge=0, le=18446744073709551615),
    ] = None
    """
    The total number of octets transmitted out of the
    interface, including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_unicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-unicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were not addressed
    to a multicast or broadcast address at this sub-layer,
    including those that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_broadcast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-broadcast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were addressed to a
    broadcast address at this sub-layer, including those
    that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_multicast_pkts: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-multicast-pkts",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were addressed to a
    multicast address at this sub-layer, including those
    that were discarded or not sent.  For a MAC-layer
    protocol, this includes both Group and Functional
    addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_discards: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:out-discards", ge=0, le=18446744073709551615
        ),
    ] = None
    """
    The number of outbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being transmitted.  One possible reason
    for discarding such a packet could be to free up buffer
    space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    out_errors: Annotated[
        int,
        Field(alias="openconfig-interfaces:out-errors", ge=0, le=18446744073709551615),
    ] = None
    """
    For packet-oriented interfaces, the number of outbound
    packets that could not be transmitted because of errors.
    For character-oriented or fixed-length interfaces, the
    number of outbound transmission units that could not be
    transmitted because of errors.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'last-clear'.
    """
    carrier_transitions: Annotated[
        int,
        Field(
            alias="openconfig-interfaces:carrier-transitions",
            ge=0,
            le=18446744073709551615,
        ),
    ] = None
    """
    Number of times the interface state has transitioned
    between up and down since the time the device restarted
    or the last-clear time, whichever is most recent.
    """
    last_clear: Annotated[
        int,
        Field(alias="openconfig-interfaces:last-clear", ge=0, le=18446744073709551615),
    ] = None
    """
    Timestamp of the last time the interface counters were
    cleared.

    The value is the timestamp in nanoseconds relative to
    the Unix Epoch (Jan 1, 1970 00:00:00 UTC).
    """


class HoldTimeContainer(BaseModel):
    """
    Top-level container for hold-time settings to enable
    dampening advertisements of interface transitions.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    state: Annotated[StateContainer2, Field(alias="openconfig-interfaces:state")] = None


class StateContainer(BaseModel):
    """
    Operational state data at the global interface level
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    name: Annotated[str, Field(alias="openconfig-interfaces:name")] = None
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
    type: Annotated[str, Field(alias="openconfig-interfaces:type")]
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
    mtu: Annotated[int, Field(alias="openconfig-interfaces:mtu", ge=0, le=65535)] = None
    """
    Set the max transmission unit size in octets
    for the physical interface.  If this is not set, the mtu is
    set to the operational default -- e.g., 1514 bytes on an
    Ethernet interface.
    """
    loopback_mode: Annotated[
        bool, Field(alias="openconfig-interfaces:loopback-mode")
    ] = False
    """
    When set to true, the interface is logically looped back,
    such that packets that are forwarded via the interface
    are received on the same interface.
    """
    description: Annotated[str, Field(alias="openconfig-interfaces:description")] = None
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
    enabled: Annotated[bool, Field(alias="openconfig-interfaces:enabled")] = True
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
    ifindex: Annotated[
        int, Field(alias="openconfig-interfaces:ifindex", ge=0, le=4294967295)
    ] = None
    """
    System assigned number for each interface.  Corresponds to
    ifIndex object in SNMP Interface MIB
    """
    admin_status: Annotated[
        AdminStatusLeaf, Field(alias="openconfig-interfaces:admin-status")
    ]
    oper_status: Annotated[
        OperStatusLeaf, Field(alias="openconfig-interfaces:oper-status")
    ]
    last_change: Annotated[
        int,
        Field(alias="openconfig-interfaces:last-change", ge=0, le=18446744073709551615),
    ] = None
    """
    This timestamp indicates the time of the last state change
    of the interface (e.g., up-to-down transition). This
    corresponds to the ifLastChange object in the standard
    interface MIB.

    The value is the timestamp in nanoseconds relative to
    the Unix Epoch (Jan 1, 1970 00:00:00 UTC).
    """
    counters: Annotated[
        CountersContainer, Field(alias="openconfig-interfaces:counters")
    ] = None


class StateContainer3(BaseModel):
    """
    Operational state data for logical interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    index: Annotated[
        int, Field(alias="openconfig-interfaces:index", ge=0, le=4294967295)
    ] = 0
    """
    The index of the subinterface, or logical interface number.
    On systems with no support for subinterfaces, or not using
    subinterfaces, this value should default to 0, i.e., the
    default subinterface.
    """
    description: Annotated[str, Field(alias="openconfig-interfaces:description")] = None
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
    enabled: Annotated[bool, Field(alias="openconfig-interfaces:enabled")] = True
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
    name: Annotated[str, Field(alias="openconfig-interfaces:name")] = None
    """
    The system-assigned name for the sub-interface.  This MAY
    be a combination of the base interface name and the
    subinterface index, or some other convention used by the
    system.
    """
    ifindex: Annotated[
        int, Field(alias="openconfig-interfaces:ifindex", ge=0, le=4294967295)
    ] = None
    """
    System assigned number for each interface.  Corresponds to
    ifIndex object in SNMP Interface MIB
    """
    admin_status: Annotated[
        AdminStatusLeaf2, Field(alias="openconfig-interfaces:admin-status")
    ]
    oper_status: Annotated[
        OperStatusLeaf2, Field(alias="openconfig-interfaces:oper-status")
    ]
    last_change: Annotated[
        int,
        Field(alias="openconfig-interfaces:last-change", ge=0, le=18446744073709551615),
    ] = None
    """
    This timestamp indicates the time of the last state change
    of the interface (e.g., up-to-down transition). This
    corresponds to the ifLastChange object in the standard
    interface MIB.

    The value is the timestamp in nanoseconds relative to
    the Unix Epoch (Jan 1, 1970 00:00:00 UTC).
    """
    counters: Annotated[
        CountersContainer2, Field(alias="openconfig-interfaces:counters")
    ] = None


class SubinterfaceListEntry(BaseModel):
    """
    The list of subinterfaces (logical interfaces) associated
    with a physical interface
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    index: Annotated[
        int, Field(alias="openconfig-interfaces:index", ge=0, le=4294967295)
    ]
    """
    The index number of the subinterface -- used to address
    the logical interface
    """
    state: Annotated[StateContainer3, Field(alias="openconfig-interfaces:state")] = None


class SubinterfacesContainer(BaseModel):
    """
    Enclosing container for the list of subinterfaces associated
    with a physical interface
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    subinterface: Annotated[
        List[SubinterfaceListEntry],
        Field(default_factory=list, alias="openconfig-interfaces:subinterface"),
    ]


class InterfaceListEntry(BaseModel):
    """
    The list of named interfaces on the device.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    name: Annotated[str, Field(alias="openconfig-interfaces:name")]
    """
    References the configured name of the interface
    """
    state: Annotated[StateContainer, Field(alias="openconfig-interfaces:state")] = None
    hold_time: Annotated[
        HoldTimeContainer, Field(alias="openconfig-interfaces:hold-time")
    ] = None
    subinterfaces: Annotated[
        SubinterfacesContainer, Field(alias="openconfig-interfaces:subinterfaces")
    ] = None


class InterfacesContainer(BaseModel):
    """
    Top level container for interfaces, including configuration
    and state data.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    interface: Annotated[
        List[InterfaceListEntry],
        Field(default_factory=list, alias="openconfig-interfaces:interface"),
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
    namespace: str = "http://openconfig.net/yang/interfaces"
    prefix: str = "oc-if"
    interfaces: Annotated[
        InterfacesContainer, Field(alias="openconfig-interfaces:interfaces")
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
