# YANG

!!! note

    This text has been gratefully copied from the Term project documentation by D. Jovicic and D. Walther.


YANG (short for "Yet Another Next Generation") is a data modeling language that was designed to improve upon the limitations of SNMP (Simple Network Management Protocol) in configuration management. While SNMP is commonly used as a network management system to detect errors on network devices, its disadvantages sparked a need for the creation of a better protocol. In 2006, the IETF published NETCONF, a standardized protocol for automating network configurations. NETCONF allows for the retrieval, upload, manipulation, and deletion of configuration data. However, NETCONF only defines the process of transmitting and modifying data, not the structure of the data itself. This lead to the to the development of YANG. YANG makes it easier to understand data models and is widely used in the networking industry.

YANG is hierarchical, provides high extensibility and can distinguish between configurations and status.
In other words, YANG complements NETCONF so that it is possible to define configuration and state data, notifications and Remote Procedure Calls using NETCONF-based operations.

A YANG module defines a single data model, however, it can reference definitions from other modules by using the `import` and `include` statements. YANG, as defined in [RFC6020](https://www.rfc-editor.org/rfc/rfc6020), has four primary node types, as shown in the table below.

| Type        | Description                                                                            | Comparable to      |
| ----------- | -------------------------------------------------------------------------------------- | ------------------ |
| `leaf`      | represents a single value                                                              | a variable         |
| `leaf-list` | contains a sequence of leaf nodes                                                      | an array           |
| `container` | contains a group of related nodes                                                      | a class            |
| `list`      | contains a sequence of nodes, each uniquely identified by one or more key attributes   | a database table   |


```yang title="YANG Model Interface Common Example"
grouping passive-interface-grouping {
  container passive-interface {
    description
      "Suppress routing updates on an interface";
    choice passive-interface-choice {
      leaf default {
        description
          "Suppress routing updates on all interfaces";
        type empty;
      }
      leaf-list interface {
        type string;
      }
    }
  }
  container disable {
    when '../passive-interface/default';
    list passive-interface {
      key "interface";
      leaf interface {
        type string;
      }
    }
  }
}
```


## typedef

By using the `typedef` statement, one can define types derived from a base type. This base type can either be a built-in type, such as `string` or `uint8`, or an already derived type. This allows for a basic form of inheritance between types, where the root type is always a built-in type.

For example, a type called `percent` can be defined, which is derived from the base type `uint8` and has its value restricted to between 0 and 100.

```yang title="typedef percent"
typedef percent {
    type uint8 {
        range "0 .. 100";
    }
}
```

Such a type can then be referenced by other statements, such as `leaf`. The `completion` leaf can be thought of as a variable of type `percent`.

```yang title="typedef percent usage example"
leaf completion {
    type percent;
}
```


## leafref

The `leafref` type is a little bit more complicated to understand than the other types.

The `leafref` type is used to reference other `leaf` instances in the tree via its "path" sub-statement. The "path" statement takes a string as an argument and must refer to an existing leaf or a `leaf-list` node, dangling references are not allowed.

```yang title="Simple leafref yang example"
list interface {
  key "name";
  leaf name {
    type string;
  }
  leaf admin-status {
    type admin-status;
  }
  list address {
    key "ip";
    leaf ip {
      type yang:ip-address;
    }
  }
}

leaf mgmt-interface {
  type leafref {
    path "../interface/name";
  }
}
```

We can see that the `leafref` refers to the path `"../interface/name"`, meaning that the leaf it is referring to can be found by leaving the scope of the current node, navigating into the "interface" list and finally locating the node called "name". A corresponding XML is shown below.

```xml title="Simple leafref XML example"
<interface>
    <name>eth0</name>
</interface>
<interface>
    <name>lo</name>
</interface>

<mgmt-interface>eth0</mgmt-interface>
```
