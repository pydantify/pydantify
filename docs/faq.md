# FAQ

## Generated model is empty

It looks like Pydantify could not find the entry point. Could it be that your model augments another model? You must use the main model and the path option to select the expected info. You can use `pyang` to visualize the tree.

??? example

      In this example the "srl nokia ntp" model augment the "srl nokia system" model.

      ```
      $ pyang -f tree -p srlinux-yang-models/ srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-ntp.yang
      srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-ntp.yang:18: warning: imported module "srl_nokia-extensions" not used
      module: srl_nokia-ntp

      augment /srl-system:system:
         +--rw ntp!
         |  +--rw admin-state?        srl-comm:admin-state
         |  +--ro oper-state?         srl-comm:oper-state
         |  +--ro synchronized?       union
         |  +--rw network-instance    -> /srl_nokia-netinst:network-instance/name
         |  +--rw source-address?     srl-comm:ip-address
         |  +--rw server* [address]
         |     +--rw address            ntp-host
         |     +--rw iburst?            boolean
         |     +--rw prefer?            boolean
         |     +--ro stratum?           uint8
         |     +--ro jitter?            uint64
         |     +--ro offset?            uint64
         |     +--ro root-delay?        uint64
         |     +--ro root-dispersion?   uint64
         |     +--ro poll-interval?     uint32
         +--rw clock
            +--rw timezone?   srl-tz:tzdata-timezone
      ```

      Using the "srl nokia system" model, the `tree-path` option can be used to only see the ntp part.
      ```
      $ pyang -f tree -p srlinux-yang-models/ srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-system.yang srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-ntp.yang
      --tree-path=system/ntp
      srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-ntp.yang:18: warning: imported module "srl_nokia-extensions" not used
      module: srl_nokia-system
      +--rw system
         +--rw srl_nokia-ntp:ntp!
            +--rw srl_nokia-ntp:admin-state?        srl-comm:admin-state
            +--ro srl_nokia-ntp:oper-state?         srl-comm:oper-state
            +--ro srl_nokia-ntp:synchronized?       union
            +--rw srl_nokia-ntp:network-instance    -> /srl_nokia-netinst:network-instance/name
            +--rw srl_nokia-ntp:source-address?     srl-comm:ip-address
            +--rw srl_nokia-ntp:server* [address]
               +--rw srl_nokia-ntp:address            ntp-host
               +--rw srl_nokia-ntp:iburst?            boolean
               +--rw srl_nokia-ntp:prefer?            boolean
               +--ro srl_nokia-ntp:stratum?           uint8
               +--ro srl_nokia-ntp:jitter?            uint64
               +--ro srl_nokia-ntp:offset?            uint64
               +--ro srl_nokia-ntp:root-delay?        uint64
               +--ro srl_nokia-ntp:root-dispersion?   uint64
               +--ro srl_nokia-ntp:poll-interval?     uint32
      ```

      Pydantify is a pyang plugin and all options not relevant for pzdantify are passed to pyang.

      ```
      $ pydantify --path=system/ntp srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-system.yang srlinux-yang-models/srlinux-yang-models/srl_nokia/models/system/srl_nokia-ntp.yang -p srlinux-yang-models/
      ```
