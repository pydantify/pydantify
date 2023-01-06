# IETF Interfaces

!!! warning

    *Pydantify* is still in an alpha state and many parts can hopefully be improved in future versions. 

## YANG Model
Using *pyang* the model can be validated and displayed as a tree.


```title="pyang -f tree ietf-interfaces.yang"
--8<-- "examples/ietf-interfaces/pyang_tree.txt"
```
!!! note

    Only the model *ietf-interfaces* is used without any models like *ietf-ip*, which augment the *ietf-interfaces* model. 

## Create pydantic model

To focus only on the configuration part of the model, the model path can be trimmed to the tree branch `ietf-interfaces:interfaces/`.

```bash
$ pydantify -t=ietf-interfaces/interfaces ietf-interfaces.yang
[INFO] /workspaces/pydantify/pydantify/plugins/pydantic_plugin.py:41 (emit): Output model generated in 0.063s.
```

The generated module will be in the file `out/out.py`. We can move and rename it to `ietf_interfaces.py`.

??? info "ietf_interfaces.py"

    ```python title="ietf_interfaces.py"
    --8<-- "examples/ietf-interfaces/ietf_interfaces.py"
    ```

## Pars JSON data into the model

Using *requests*, or any other HTTP library, the data can be retrieved in JSON format.

```python title="restconf.py" linenums="24"
--8<-- "examples/ietf-interfaces/restconf.py:24:26"
```

The output depends on the network device. This example uses a Cisco CSR1k with three interfaces.

```json title="restconf data"
{
  "ietf-interfaces:interfaces": {
    "interface": [
      {
        "name": "GigabitEthernet1",
        "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": true,
        "ietf-ip:ipv4": {
          "address": [
            {
              "ip": "10.10.20.48",
              "netmask": "255.255.255.0"
            }
          ]
        },
        "ietf-ip:ipv6": {}
      },
      {
        "name": "GigabitEthernet2",
        "description": "https://pydantify.github.io/pydantify/",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": true,
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {}
      },
      {
        "name": "GigabitEthernet3",
        "description": "Configured and Merged by Ansible Network",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": false,
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {}
      }
    ]
  }
}
```

The received response from the device includes data from the *ietf-ip* model, which augment the *ietf-interfaces* model. Because the build model does not have these fields, the model configuration must be set to **ignore** extra fields.

```python title="restconf.py" linenums="30"
--8<-- "examples/ietf-interfaces/restconf.py:30:36"
```

Now the model is filled with the received data. By using the option `by_alias=True`, all keys contain the model prefix in the output.

```json title="model output"
{
  "ietf-interfaces:interfaces": {
    "ietf-interfaces:interface": [
      {
        "ietf-interfaces:name": "GigabitEthernet1",
        "ietf-interfaces:description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
        "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
        "ietf-interfaces:enabled": true
      },
      {
        "ietf-interfaces:name": "GigabitEthernet2",
        "ietf-interfaces:description": "Configured and Merged by Ansible Network",
        "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
        "ietf-interfaces:enabled": false
      },
      {
        "ietf-interfaces:name": "GigabitEthernet3",
        "ietf-interfaces:description": "Configured and Merged by Ansible Network",
        "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
        "ietf-interfaces:enabled": false
      }
    ]
  }
}
```

As with all Python objects, you can access them and make evaluations.

??? info "`__root__`"

    For now, to access the value of the leaf object, the variable `__root__` needs to be used. Hopefully we can improve this in future versions.

```python title="restconf.py" linenums="41"
--8<-- "examples/ietf-interfaces/restconf.py:41:47"
```

The first interface is the management interface and is enabled; the other two are disabled.

``` title="Interface status"
Interface GigabitEthernet1 is enabled
Interface GigabitEthernet2 is disabled
Interface GigabitEthernet3 is disabled
```

## Update/change model

This example takes the second interface, changes the interface to enable, and updates the description.

```python title="restconf.py" linenums="50"
--8<-- "examples/ietf-interfaces/restconf.py:50:57"
```

Taking a look at only this level of the tree, the generated output contains the changes.

```json title="updated interface"
{
  "ietf-interfaces:name": "GigabitEthernet2",
  "ietf-interfaces:description": "https://pydantify.github.io/pydantify/",
  "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
  "ietf-interfaces:enabled": true
}
```

For an easy configuration update, a new model can be created only containing the changed interface.

```python title="restconf.py" linenums="61"
--8<-- "examples/ietf-interfaces/restconf.py:61:62"
```

Now the output contains all layers of the YANG tree starting at the root interfaces field.

```json title="new model output"
{
  "ietf-interfaces:interfaces": {
    "ietf-interfaces:interface": [
      {
        "ietf-interfaces:name": "GigabitEthernet2",
        "ietf-interfaces:description": "https://pydantify.github.io/pydantify/",
        "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
        "ietf-interfaces:enabled": true
      }
    ]
  }
}
```

## Update device configuration

Using the newly created model from the top, a *PATCH* request can be sent to the device using the root URL of the model (same URL was used to get the data).

??? info "exclude_defaults=True"

    It is recommended to use the option `exlude_defaults=True` not to send unnecessary data.

```python title="restconf.py" linenums="66"
--8<-- "examples/ietf-interfaces/restconf.py:66:69"
```

To address the interface directly using the URL, to not only update but also be able to replace the configuration, the data structure needs not a map containing a list of interfaces but a map containing a map looking like this:

```json title="JSON paylod to address interface direclty"
{
  "ietf-interfaces:interface": {
    "ietf-interfaces:name": "GigabitEthernet2",
    "ietf-interfaces:description": "https://pydantify.github.io/pydantify/",
    "ietf-interfaces:type": "iana-if-type:ethernetCsmacd",
    "ietf-interfaces:enabled": true,
  }
}
```

Now the URL must include the interface like `ietf-interfaces:interfaces/interface=GigabitEthernet2`.

```python title="restconf.py" linenums="74"
--8<-- "examples/ietf-interfaces/restconf.py:74:81"
```
