# Hello World

## YANG Model

For a "Hello World" example let's take a simple yang model. This model allows specifying a simple endpoint containing an address and port. An optional description can be defined.

```yang title="my-endpoint.yang"
--8<-- "examples/hello_world/my-endpoint.yang"
```

Using `pyang` the model can be validated and displayed as a tree.


```title="pyang -f tree my-endpoint.yang"
--8<-- "examples/hello_world/pyang_tree.txt"
```

## Create pydantic model

`pydantify` can now be used to convert the YANG model into a `pydantic` model.

```bash
$ pydantify examples/hello_world/my-endpoint.yang 
[INFO] /workspaces/pydantify/pydantify/plugins/pydantic_plugin.py:41 (emit): Output model generated in 0.049s.
```

The generated module will be in the file `out/out.py`. We can move and rename it to `endpoint.py`

```python title="endpoint.py"
--8<-- "examples/hello_world/endpoint.py"
```


## Using the model

```python title="create_json.py"
--8<-- "examples/hello_world/create_json.py:3:10"
```

```json title="endpoint1.json"
--8<-- "examples/hello_world/endpoint1.json"
```


```python title="create_json.py"
--8<-- "examples/hello_world/create_json.py:15:15"
```

```json title="endpoint1_json_exclude_default_and_by_alias.json"
--8<-- "examples/hello_world/endpoint1_json_exclude_default_and_by_alias.json"
```

```python title="create_json.py"
--8<-- "examples/hello_world/create_json.py:20:25"
```

```json title="endpoint2.json"
--8<-- "examples/hello_world/endpoint2.json"
```


```python title="create_json.py"
--8<-- "examples/hello_world/create_json.py:30:31"
```

```json title="endpoint3.json"
--8<-- "examples/hello_world/endpoint3.json"
```


```python title="create_json.py"
--8<-- "examples/hello_world/create_json.py:36:37"
```

```json title="endpoint4.json"
--8<-- "examples/hello_world/endpoint4.json"
```
