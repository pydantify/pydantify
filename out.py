from __future__ import annotations

from pydantic import BaseModel, Field


class OpenconfigInterfacesCounters(BaseModel):
    in_broadcast_pkts: str = Field(..., alias='in-broadcast-pkts')
    in_discards: str = Field(..., alias='in-discards')
    in_errors: str = Field(..., alias='in-errors')
    in_fcs_errors: str = Field(..., alias='in-fcs-errors')
    in_multicast_pkts: str = Field(..., alias='in-multicast-pkts')
    in_octets: str = Field(..., alias='in-octets')
    in_unicast_pkts: str = Field(..., alias='in-unicast-pkts')
    out_broadcast_pkts: str = Field(..., alias='out-broadcast-pkts')
    out_discards: str = Field(..., alias='out-discards')
    out_errors: str = Field(..., alias='out-errors')
    out_multicast_pkts: str = Field(..., alias='out-multicast-pkts')
    out_octets: str = Field(..., alias='out-octets')
    out_unicast_pkts: str = Field(..., alias='out-unicast-pkts')


class Model(BaseModel):
    openconfig_interfaces_admin_status: str = Field(
        ..., alias='openconfig-interfaces:admin-status'
    )
    openconfig_interfaces_counters: OpenconfigInterfacesCounters = Field(
        ..., alias='openconfig-interfaces:counters'
    )
    openconfig_interfaces_description: str = Field(
        ..., alias='openconfig-interfaces:description'
    )
    openconfig_interfaces_enabled: str = Field(
        ..., alias='openconfig-interfaces:enabled'
    )
    openconfig_platform_port_hardware_port: str = Field(
        ..., alias='openconfig-platform-port:hardware-port'
    )
    openconfig_interfaces_ifindex: int = Field(
        ..., alias='openconfig-interfaces:ifindex'
    )
    arista_intf_augments_inactive: str = Field(
        ..., alias='arista-intf-augments:inactive'
    )
    openconfig_interfaces_last_change: str = Field(
        ..., alias='openconfig-interfaces:last-change'
    )
    openconfig_interfaces_loopback_mode: str = Field(
        ..., alias='openconfig-interfaces:loopback-mode'
    )
    openconfig_interfaces_mtu: int = Field(..., alias='openconfig-interfaces:mtu')
    openconfig_interfaces_name: str = Field(..., alias='openconfig-interfaces:name')
    openconfig_interfaces_oper_status: str = Field(
        ..., alias='openconfig-interfaces:oper-status'
    )
    openconfig_vlan_tpid: str = Field(..., alias='openconfig-vlan:tpid')
    openconfig_interfaces_type: str = Field(..., alias='openconfig-interfaces:type')
