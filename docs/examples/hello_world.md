# Hello World

## YANG Model
Let's take a simple yang model for a "Hello World" example. This model allows specifying a simple endpoint containing an address and port. An optional description can be defined.

```yang title="my-endpoint.yang"
--8<-- "examples/hello_world/my-endpoint.yang"
```

Using *pyang* the model can be validated and displayed as a tree.


```title="pyang -f tree my-endpoint.yang"
--8<-- "examples/hello_world/pyang_tree.txt"
```

## Create pydantic model

*Pydantify* can now convert the YANG model into a *pydantic* one.

```bash
$ pydantify examples/hello_world/my-endpoint.yang 
[INFO] /workspaces/pydantify/pydantify/plugins/pydantic_plugin.py:41 (emit): Output model generated in 0.049s.
```

The generated module will be in the file `out/out.py`. We can move and rename it to `endpoint.py`.

```python title="endpoint.py"
--8<-- "examples/hello_world/endpoint.py"
```


## Using the model

The model can now be used as any other *pydantic* python model, and *pydantify* is not required if we don't use helper functions from *pydantify*.

The model can be imported, and Python objects can be created. The IDE (like Visual Studio Code) will offer code completion.

```python title="create_json.py" linenums="3"
--8<-- "examples/hello_world/create_json.py:3:10"
```

After creating the objects `port` and `host`, the model is instantiated with the passed objects. The *pydantic* model object can generate JSON directly by calling `.json()`.

By default, the JSON output will include all values. Using the argument `exlude_defaults=True` will not show these values. In this example, the `description` leaf is optional and has, therefore, a default value of `Null`. 

```python title="create_json.py" linenums="15"
--8<-- "examples/hello_world/create_json.py:15:15"
```

With the option `by_alias` the JSON includes the YANG module name in the keys.

```json title="endpoint1_json_exclude_default_and_by_alias.json"
--8<-- "examples/hello_world/endpoint1_json_exclude_default_and_by_alias.json"
```

Model objects containing only a `__root__` field can be created automatically. So, instead of creating a port object, specify the value in the argument of the `EndpointContainer` creation. *Pydantic* creates objects automatically in the background. More information can be found in the *pydantic* documentation for [Custom Root Types](https://docs.pydantic.dev/usage/models/#custom-root-types)

```python title="create_json.py" linenums="20"
--8<-- "examples/hello_world/create_json.py:20:25"
```

```json title="endpoint2.json"
--8<-- "examples/hello_world/endpoint2.json"
```

A Python dictionary can also be used to create nested model objects:

```python title="create_json.py" linenums="30"
--8<-- "examples/hello_world/create_json.py:30:31"
```

```json title="endpoint3.json"
--8<-- "examples/hello_world/endpoint3.json"
```

Using dictionary unpacking, the first level of the dictionary needs to match the field names of the model. Inside the model, also the alias name can be used.

```python title="create_json.py" linenums="36"
--8<-- "examples/hello_world/create_json.py:36:39"
```

```json title="endpoint4.json"
--8<-- "examples/hello_world/endpoint4.json"
```

To be able to use the alias also on the top level, the static class functions `parse_obj`, `parse_file`, or `parse_raw` can be used:

```python title="create_json.py" linenums="43"
--8<-- "examples/hello_world/create_json.py:43:51"
```

```json title="endpoint5.json"
--8<-- "examples/hello_world/endpoint5.json"
```