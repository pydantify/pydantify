# Augment

## tree

```bash
$ pyang -f tree configuration.yang namespaces.yang interfaces.yang
module: configuration
  +--rw configuration
     +--rw devicename       string
     +--rw ns:namespaces* [name]
        +--rw ns:name          string
        +--rw if:interfaces* [name]
           +--rw if:name    string
           +--rw if:ip?     string
```

## sample-xml-skeleton

```bash
$ pyang -f sample-xml-skeleton configuration.yang namespaces.yang interfaces.yang
<?xml version='1.0' encoding='UTF-8'?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <configuration xmlns="http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration">
    <devicename/>
    <namespaces xmlns="http://pydantify.github.io/ns/yang/pydantify-multimodel-namespaces">
      <name/>
      <interfaces xmlns="http://pydantify.github.io/ns/yang/pydantify-multimodel-interfaces">
        <name/>
        <ip/>
      </interfaces>
    </namespaces>
  </configuration>
</data>
```
