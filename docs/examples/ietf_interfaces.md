# IETF Interfaces

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
