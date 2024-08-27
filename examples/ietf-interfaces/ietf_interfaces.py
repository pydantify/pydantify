from __future__ import annotations

from enum import Enum
from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class Counter32Type(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=4294967295)]
    """
    The counter32 type represents a non-negative integer
    that monotonically increases until it reaches a
    maximum value of 2^32-1 (4294967295 decimal), when it
    wraps around and starts increasing again from zero.

    Counters have no defined 'initial' value, and thus, a
    single value of a counter has (in general) no information
    content.  Discontinuities in the monotonically increasing
    value normally occur at re-initialization of the
    management system, and at other times as specified in the
    description of a schema node using this type.  If such
    other times can occur, for example, the creation of
    a schema node of type counter32 at times other than
    re-initialization, then a corresponding schema node
    should be defined, with an appropriate type, to indicate
    the last discontinuity.

    The counter32 type should not be used for configuration
    schema nodes.  A default statement SHOULD NOT be used in
    combination with the type counter32.

    In the value set and its semantics, this type is equivalent
    to the Counter32 type of the SMIv2.
    """


class Counter64Type(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=18446744073709551615)]
    """
    The counter64 type represents a non-negative integer
    that monotonically increases until it reaches a
    maximum value of 2^64-1 (18446744073709551615 decimal),
    when it wraps around and starts increasing again from zero.

    Counters have no defined 'initial' value, and thus, a
    single value of a counter has (in general) no information
    content.  Discontinuities in the monotonically increasing
    value normally occur at re-initialization of the
    management system, and at other times as specified in the
    description of a schema node using this type.  If such
    other times can occur, for example, the creation of
    a schema node of type counter64 at times other than
    re-initialization, then a corresponding schema node
    should be defined, with an appropriate type, to indicate
    the last discontinuity.

    The counter64 type should not be used for configuration
    schema nodes.  A default statement SHOULD NOT be used in
    combination with the type counter64.

    In the value set and its semantics, this type is equivalent
    to the Counter64 type of the SMIv2.
    """


class DateAndTimeType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern='^(?=^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|[\\+\\-]\\d{2}:\\d{2})$).*$'
        ),
    ]
    """
    The date-and-time type is a profile of the ISO 8601
    standard for representation of dates and times using the
    Gregorian calendar.  The profile is defined by the
    date-time production in Section 5.6 of RFC 3339.

    The date-and-time type is compatible with the dateTime XML
    schema type with the following notable exceptions:

    (a) The date-and-time type does not allow negative years.

    (b) The date-and-time time-offset -00:00 indicates an unknown
        time zone (see RFC 3339) while -00:00 and +00:00 and Z
        all represent the same time zone in dateTime.

    (c) The canonical format (see below) of data-and-time values
        differs from the canonical format used by the dateTime XML
        schema type, which requires all times to be in UTC using
        the time-offset 'Z'.

    This type is not equivalent to the DateAndTime textual
    convention of the SMIv2 since RFC 3339 uses a different
    separator between full-date and full-time and provides
    higher resolution of time-secfrac.

    The canonical format for date-and-time values with a known time
    zone uses a numeric time zone offset that is calculated using
    the device's configured known offset to UTC time.  A change of
    the device's offset to UTC time will cause date-and-time values
    to change accordingly.  Such changes might happen periodically
    in case a server follows automatically daylight saving time
    (DST) time zone offset changes.  The canonical format for
    date-and-time values with an unknown time zone (usually
    referring to the notion of local time) uses the time-offset
    -00:00.
    """


class DescriptionLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title='DescriptionLeaf')]
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


class DiscontinuityTimeLeaf(RootModel[DateAndTimeType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[DateAndTimeType, Field(title='Discontinuity-timeLeaf')]
    """
    The time on the most recent occasion at which any one or
    more of this interface's counters suffered a
    discontinuity.  If no such discontinuities have occurred
    since the last re-initialization of the local management
    subsystem, then this node contains the time the local
    management subsystem re-initialized itself.
    """


class EnabledLeaf(RootModel[bool]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[bool, Field(title='EnabledLeaf')]
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


class Gauge64Type(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=18446744073709551615)]
    """
    The gauge64 type represents a non-negative integer, which
    may increase or decrease, but shall never exceed a maximum
    value, nor fall below a minimum value.  The maximum value
    cannot be greater than 2^64-1 (18446744073709551615), and
    the minimum value cannot be smaller than 0.  The value of
    a gauge64 has its maximum value whenever the information
    being modeled is greater than or equal to its maximum
    value, and has its minimum value whenever the information
    being modeled is smaller than or equal to its minimum value.
    If the information being modeled subsequently decreases
    below (increases above) the maximum (minimum) value, the
    gauge64 also decreases (increases).

    In the value set and its semantics, this type is equivalent
    to the CounterBasedGauge64 SMIv2 textual convention defined
    in RFC 2856
    """


class IfIndexLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=1, le=2147483647, title='If-indexLeaf')]
    """
    The ifIndex value for the ifEntry represented by this
    interface.
    """


class InBroadcastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='In-broadcast-pktsLeaf')]
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a broadcast
    address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class InDiscardsLeaf(RootModel[Counter32Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter32Type, Field(title='In-discardsLeaf')]
    """
    The number of inbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being deliverable to a higher-layer
    protocol.  One possible reason for discarding such a
    packet could be to free up buffer space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class InErrorsLeaf(RootModel[Counter32Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter32Type, Field(title='In-errorsLeaf')]
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
    'discontinuity-time'.
    """


class InMulticastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='In-multicast-pktsLeaf')]
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were addressed to a multicast
    address at this sub-layer.  For a MAC-layer protocol,
    this includes both Group and Functional addresses.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class InOctetsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='In-octetsLeaf')]
    """
    The total number of octets received on the interface,
    including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class InUnicastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='In-unicast-pktsLeaf')]
    """
    The number of packets, delivered by this sub-layer to a
    higher (sub-)layer, that were not addressed to a
    multicast or broadcast address at this sub-layer.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class InUnknownProtosLeaf(RootModel[Counter32Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter32Type, Field(title='In-unknown-protosLeaf')]
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
    'discontinuity-time'.
    """


class LastChangeLeaf(RootModel[DateAndTimeType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[DateAndTimeType, Field(title='Last-changeLeaf')]
    """
    The time the interface entered its current operational
    state.  If the current state was entered prior to the
    last re-initialization of the local network management
    subsystem, then this node is not present.
    """


class NameLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title='NameLeaf')]
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


class NameLeaf2(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: str
    """
    The name of the interface.

    A server implementation MAY map this leaf to the ifName
    MIB object.  Such an implementation needs to use some
    mechanism to handle the differences in size and characters
    allowed between this leaf and ifName.  The definition of
    such a mechanism is outside the scope of this document.
    """


class OutBroadcastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='Out-broadcast-pktsLeaf')]
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were addressed to a
    broadcast address at this sub-layer, including those
    that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class OutDiscardsLeaf(RootModel[Counter32Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter32Type, Field(title='Out-discardsLeaf')]
    """
    The number of outbound packets that were chosen to be
    discarded even though no errors had been detected to
    prevent their being transmitted.  One possible reason
    for discarding such a packet could be to free up buffer
    space.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class OutErrorsLeaf(RootModel[Counter32Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter32Type, Field(title='Out-errorsLeaf')]
    """
    For packet-oriented interfaces, the number of outbound
    packets that could not be transmitted because of errors.
    For character-oriented or fixed-length interfaces, the
    number of outbound transmission units that could not be
    transmitted because of errors.




    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class OutMulticastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='Out-multicast-pktsLeaf')]
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
    'discontinuity-time'.
    """


class OutOctetsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='Out-octetsLeaf')]
    """
    The total number of octets transmitted out of the
    interface, including framing characters.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class OutUnicastPktsLeaf(RootModel[Counter64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Counter64Type, Field(title='Out-unicast-pktsLeaf')]
    """
    The total number of packets that higher-level protocols
    requested be transmitted, and that were not addressed
    to a multicast or broadcast address at this sub-layer,
    including those that were discarded or not sent.

    Discontinuities in the value of this counter can occur
    at re-initialization of the management system, and at
    other times as indicated by the value of
    'discontinuity-time'.
    """


class PhysAddressType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern='^(?=^([0-9a-fA-F]{2}(:[0-9a-fA-F]{2})*)?$).*$')]
    """
    Represents media- or physical-level addresses represented
    as a sequence octets, each octet represented by two hexadecimal
    numbers.  Octets are separated by colons.  The canonical
    representation uses lowercase characters.

    In the value set and its semantics, this type is equivalent
    to the PhysAddress textual convention of the SMIv2.
    """


class SpeedLeaf(RootModel[Gauge64Type]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Gauge64Type, Field(title='SpeedLeaf')]
    """
    An estimate of the interface's current bandwidth in bits
    per second.  For interfaces that do not vary in
    bandwidth or for those where no accurate estimation can
    be made, this node should contain the nominal bandwidth.
    For interfaces that have no concept of bandwidth, this
    node is not present.
    """


class StatisticsContainer(BaseModel):
    """
    A collection of interface-related statistics objects.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    discontinuity_time: Annotated[
        DiscontinuityTimeLeaf, Field(alias='ietf-interfaces:discontinuity-time')
    ]
    in_octets: Annotated[InOctetsLeaf, Field(None, alias='ietf-interfaces:in-octets')]
    in_unicast_pkts: Annotated[
        InUnicastPktsLeaf, Field(None, alias='ietf-interfaces:in-unicast-pkts')
    ]
    in_broadcast_pkts: Annotated[
        InBroadcastPktsLeaf, Field(None, alias='ietf-interfaces:in-broadcast-pkts')
    ]
    in_multicast_pkts: Annotated[
        InMulticastPktsLeaf, Field(None, alias='ietf-interfaces:in-multicast-pkts')
    ]
    in_discards: Annotated[
        InDiscardsLeaf, Field(None, alias='ietf-interfaces:in-discards')
    ]
    in_errors: Annotated[InErrorsLeaf, Field(None, alias='ietf-interfaces:in-errors')]
    in_unknown_protos: Annotated[
        InUnknownProtosLeaf, Field(None, alias='ietf-interfaces:in-unknown-protos')
    ]
    out_octets: Annotated[
        OutOctetsLeaf, Field(None, alias='ietf-interfaces:out-octets')
    ]
    out_unicast_pkts: Annotated[
        OutUnicastPktsLeaf, Field(None, alias='ietf-interfaces:out-unicast-pkts')
    ]
    out_broadcast_pkts: Annotated[
        OutBroadcastPktsLeaf, Field(None, alias='ietf-interfaces:out-broadcast-pkts')
    ]
    out_multicast_pkts: Annotated[
        OutMulticastPktsLeaf, Field(None, alias='ietf-interfaces:out-multicast-pkts')
    ]
    out_discards: Annotated[
        OutDiscardsLeaf, Field(None, alias='ietf-interfaces:out-discards')
    ]
    out_errors: Annotated[
        OutErrorsLeaf, Field(None, alias='ietf-interfaces:out-errors')
    ]


class TypeLeaf(RootModel[Any]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Any, Field(title='TypeLeaf')]
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


class TypeLeaf2(RootModel[Any]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[Any, Field(title='TypeLeaf2')]
    """
    The type of the interface.
    """


class EnumerationEnum(Enum):
    integer_1 = 1
    integer_2 = 2


class EnumerationEnum2(Enum):
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3


class EnumerationEnum3(Enum):
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3
    integer_4 = 4
    integer_5 = 5
    integer_6 = 6
    integer_7 = 7


class AdminStatusLeaf(RootModel[EnumerationEnum2]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[EnumerationEnum2, Field(title='Admin-statusLeaf')]
    """
    The desired state of the interface.

    This leaf has the same read semantics as ifAdminStatus.
    """


class InterfaceStateRefType(RootModel[NameLeaf2]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: NameLeaf2
    """
    This type is used by data models that need to reference
    the operationally present interfaces.
    """


class LinkUpDownTrapEnableLeaf(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[EnumerationEnum, Field(title='Link-up-down-trap-enableLeaf')]
    """
    Controls whether linkUp/linkDown SNMP notifications
    should be generated for this interface.

    If this node is not configured, the value 'enabled' is
    operationally used by the server for interfaces that do
    not operate on top of any other interface (i.e., there are
    no 'lower-layer-if' entries), and 'disabled' otherwise.
    """


class LowerLayerIfLeafList(RootModel[InterfaceStateRefType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[InterfaceStateRefType, Field(title='Lower-layer-ifLeafList')]
    """
    A list of references to interfaces layered underneath this
    interface.
    """


class OperStatusLeaf(RootModel[EnumerationEnum3]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[EnumerationEnum3, Field(title='Oper-statusLeaf')]
    """
    The current operational state of the interface.

    This leaf has the same semantics as ifOperStatus.
    """


class PhysAddressLeaf(RootModel[PhysAddressType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[PhysAddressType, Field(title='Phys-addressLeaf')]
    """
    The interface's address at its protocol sub-layer.  For
    example, for an 802.x interface, this object normally
    contains a Media Access Control (MAC) address.  The
    interface's media-specific modules must define the bit


    and byte ordering and the format of the value of this
    object.  For interfaces that do not have such an address
    (e.g., a serial line), this node is not present.
    """


class HigherLayerIfLeafList(RootModel[InterfaceStateRefType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[InterfaceStateRefType, Field(title='Higher-layer-ifLeafList')]
    """
    A list of references to interfaces layered on top of this
    interface.
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

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[NameLeaf, Field(None, alias='ietf-interfaces:name')]
    description: Annotated[
        DescriptionLeaf, Field(None, alias='ietf-interfaces:description')
    ]
    type: Annotated[TypeLeaf, Field(alias='ietf-interfaces:type')]
    enabled: Annotated[EnabledLeaf, Field(True, alias='ietf-interfaces:enabled')]
    link_up_down_trap_enable: Annotated[
        LinkUpDownTrapEnableLeaf,
        Field(None, alias='ietf-interfaces:link-up-down-trap-enable'),
    ]


class InterfaceListEntry2(BaseModel):
    """
    The list of interfaces on the device.

    System-controlled interfaces created by the system are
    always present in this list, whether they are configured or
    not.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[NameLeaf2, Field(None, alias='ietf-interfaces:name')]
    type: Annotated[TypeLeaf2, Field(alias='ietf-interfaces:type')]
    admin_status: Annotated[
        AdminStatusLeaf, Field(alias='ietf-interfaces:admin-status')
    ]
    oper_status: Annotated[OperStatusLeaf, Field(alias='ietf-interfaces:oper-status')]
    last_change: Annotated[
        LastChangeLeaf, Field(None, alias='ietf-interfaces:last-change')
    ]
    if_index: Annotated[IfIndexLeaf, Field(alias='ietf-interfaces:if-index')]
    phys_address: Annotated[
        PhysAddressLeaf, Field(None, alias='ietf-interfaces:phys-address')
    ]
    higher_layer_if: Annotated[
        List[HigherLayerIfLeafList], Field([], alias='ietf-interfaces:higher-layer-if')
    ]
    """
    A list of references to interfaces layered on top of this
    interface.
    """
    lower_layer_if: Annotated[
        List[LowerLayerIfLeafList], Field([], alias='ietf-interfaces:lower-layer-if')
    ]
    """
    A list of references to interfaces layered underneath this
    interface.
    """
    speed: Annotated[SpeedLeaf, Field(None, alias='ietf-interfaces:speed')]
    statistics: Annotated[
        StatisticsContainer, Field(None, alias='ietf-interfaces:statistics')
    ]


class InterfacesStateContainer(BaseModel):
    """
    Data nodes for the operational state of interfaces.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    interface: Annotated[
        List[InterfaceListEntry2], Field(alias='ietf-interfaces:interface')
    ]


class InterfacesContainer(BaseModel):
    """
    Interface configuration parameters.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    interface: Annotated[
        List[InterfaceListEntry], Field(alias='ietf-interfaces:interface')
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
    interfaces: Annotated[
        InterfacesContainer, Field(None, alias='ietf-interfaces:interfaces')
    ]
    interfaces_state: Annotated[
        InterfacesStateContainer, Field(None, alias='ietf-interfaces:interfaces-state')
    ]


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