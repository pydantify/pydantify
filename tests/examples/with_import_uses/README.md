# Import Uses

## tree

```bash
$ pyang -f tree configuration.yang
module: configuration
  +--rw configuration
     +--rw devicename    string
     +--rw namespaces* [name]
        +--rw name          string
        +--rw interfaces* [name]
           +--rw name    string
           +--rw ip?     string
```

## sample-xml-skeleton

```bash
pyang -f sample-xml-skeleton configuration.yang
<?xml version='1.0' encoding='UTF-8'?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <configuration xmlns="http://pydantify.github.io/ns/yang/pydantify-multimodel-configuration">
    <devicename/>
    <namespaces>
      <name/>
      <interfaces>
        <name/>
        <ip/>
      </interfaces>
    </namespaces>
  </configuration>
</data>
```
