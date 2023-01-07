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


## RESTCONF

We took a short excursion into the history of the creation of NETCONF and YANG, but there is one more component to it - the RESTCONF protocol. RESTCONF is a protocol based on HTTP that provides an interface to access data defined in YANG, while using the data store concepts of NETCONF.

The goal of both YANG, NETCONF and RESTCONF is to facilitate the automation of network configurations. While NETCONF is based on RPC (Remote Procedure Call), something many companies would need to re-train their IT-Engineers for in order to use, RESTCONF uses HTTP-based RESTful APIs, which are much more ubiquitous in the industry.

RESTCONF tends to be easier to work with for simple CRUD operations when compared to NETCONF, and its ability to work with both XML and JSON data makes it a bit more flexible to integrate with other software, such as in our case.

All in all, RESTCONF is an easy way for applications to access configuration and state data, data-model-specific RPC operations, and event notifications.

The operations provided by RESTCONF are defined in [RFC8040](https://www.rfc-editor.org/rfc/rfc8040.html) and can be summarized thusly:

- **OPTIONS**
    * Is sent to discover which methods (options) are supported by the opposing side for a specified resource
- **GET**
    * Is sent to retrieve data and metadata of a specified resource
- **HEAD**
    * Is sent to retrieve just the header fields from a specified resource
- **POST**
    * Is sent by the client to create a data resource or invoke a Remote Procedure Call
- **PUT**
    * Is sent to create or replace the data of a specified resource
- **PATCH**
    * Is used to provide an extensible framework for resource patching mechanisms and can be used to create or modify a child resource within the specified resource
- **DELETE**
    * Is used to delete the specified resource


## XPath

XML Path Language, or XPath for short, was designed to support the query of XML structures. The simplest form an XPath statement can take would be a complete and internal path, such as `interfaces/ip`, which selects a child node called `ip` located in a node called `interfaces`. There are many, much more complex queries that can be performed through XPath, an introduction to which can be found on the [W3Schools](https://www.w3schools.com/xml/xpath_intro.asp) website.

In YANG, XPath is used in for referencing other nodes or to specify restrictions on them.
Here are a few examples of where XPath finds application in YANG:

**Must Statements** are used to constraint nodes; in the example below, we want to make sure that the value of `count` is exactly 10.

```yang title="XPath must statement"
container interface {
    must "count = 10";
    leaf count {
        type uint8
    }
}
```

**If/When Statements** are used to make instances of YANG conditional. The `when` statements can change at run-time, whereas `if` statements are set on boot-time.
The YANG example describes a `leaf` called "name", which is only present in the data if the value of `percent` is below 50.

```yang title="XPath when statement"
container test {
    leaf percent {
        type uint8
    }
    leaf name {
        when "../percent < 50";
        type string
    }
}
```


**Path Statements**, as described in the section leafref, are the most common application of XPath within YANG. They are essential for the functioning of leafrefs as they specify which YANG node is being referenced. They can also be used to add additional restrictions on the properties the node to be referenced must have, allowing them to be used as a form of *foreign key constraint*.


### XPath in Pydantify
All in all, XPath is a powerful feature, but making use of it is not a trivial affair. For instance the `path` statements can only be checked as the model is being instantiated with data, meaning that the validity of the input can only be tested after Pydantify has already completed its task of generating a pydantic output model.

In addition, queries like `if` and `when` can alter which components are included in the model dynamically based on input values. To fully reproduce this behaviour in the output model would require the output model to be self-modifying, adding a layer of meta-programming which would easily exceed the scope of our project.

It would however be possible to validate the input after the instantiation of the output model by having *pyang* check the generated RESTCONF payload against the YANG model. This would allows the the configuration data to be validated fully, without having to implement the validation ourselves. The only downside being that the YANG files have to be preserved alongside the output model in order to provide this functionality.
