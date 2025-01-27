# Pydantify
A ***prototype*** CLI tool to transform YANG models into Pydantic datastructures that can be initialized with config values and serialized into RESTCONF payloads.

[Check out the documentation https://pydantify.github.io/pydantify/](https://pydantify.github.io/pydantify/)

## For users
### Installation
**Prerequisites:**
- Python 3.10
- pip

**Installing from PYPI:**
```bash
pip install pydantify
```

**Installing from local folder:**
```bash
pip install .
```

### Usage
**Example:**
```ps
pydantify -i ./models_dir -o ./output_dir -t interfaces/ethernet model.yang
```
Transforms the `/interfaces/ethernet` node and its children (located in `model.yang`) into a Python script located in `./output_dir`. Imports of definitions found in `./models_dir` are included if relevant to the specified model and node.

**Command syntax:**
```ps
pydantify [-h] [-v] [-V] [-S] [-i INPUT_DIR] [-o OUTPUT_DIR] [-t TRIM_PATH] input_file

positional arguments:
  input_file            The YANG file containing the entrypoint to the model to evaluate.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enables debug output
  -V, --include-verification
                        Adds validation code, as well as the relevant YANG files, to the output model.
  -S, --standalone      Generated output model has no dependency on Pydantify.
                        All required code is copied into the output model.
  -i INPUT_DIR, --input-dir INPUT_DIR, --path INPUT_DIR
                        The directory that contains the YANG input model.
                        Defaults to the input file's folder.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The directory that should be used to store the output model. Defaults to "$CWD/out".
  -f OUTPUT_FILE, --output-file OUTPUT_FILE
                        The name of the output file. Defaults to "out.py".
  -t TRIM_PATH, --trim-path TRIM_PATH
                        Get only the specified branch of the whole tree.

NOTE: All unknown arguments will be passed to Pyang as-is and without guarantees.
```

---
## For developers
### Requirements:
- Visual Studio Code
- Python 3.10
- [PDM package manager](https://pdm.fming.dev/)

### Instructions:
**Note**: instructions with the same indentation are alternatives to eachother.
- Install
    - dependencies through pdm (`pdm install` in project root)
        - into the local `__pypackages__` folder
            - to run your project as a python module
                - locally (`python -m pydantify`)
                - in a docker container (see [Dockerfile](./Dockerfile))
            - to be accessed by your IDE for intellisense (see [.vscode/settings.json](./.vscode/settings.json))
            - to be accessed by your debug launch configuration (see [.vscode/launch.json](./.vscode/launch.json))
    - project through pip ([see guide for users](#for-users))
- Build
    - through pdm (`pdm build`)
        - into the local `dist` folder
            - to be published on pypi
                - through twine (`twine upload dist/*`)

---

## Links relevant to project
### Pydantic
- [source](https://github.com/pydantic/pydantic)
- [documentation](https://pydantic-docs.helpmanual.io/)

### Explanations
- [Yang concepts (yangson)](https://yangson.labs.nic.cz/concepts-terms.html)
- [yang-python training examples](https://github.com/cmoberg/netconf-yang-training)

### Yang models
- [YangModels/yang](https://github.com/YangModels/yang)

### Pyang
- [pyang](https://github.com/mbj4668/pyang)


---
## Thanks

- Dejan Jovicic and Dominic Walther, who laid the foundations of pydantify
