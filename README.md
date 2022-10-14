## Assignment
- [PDF](https://gitlab.ost.ch/ins-stud/model-driven-network-automation/assignment/-/jobs/618674/artifacts/file/Make-Model-Driven-Network-Automation-Pythonic_v1.0.pdf)

## Pydantic
- [source](https://github.com/pydantic/pydantic)
- [documentation](https://pydantic-docs.helpmanual.io/)

## Explanations
- [Yang concepts (yangson)](https://yangson.labs.nic.cz/concepts-terms.html)
- [yang-python training examples](https://github.com/cmoberg/netconf-yang-training)

## Yang models
- [YangModels/yang](https://github.com/YangModels/yang): Yang models galore

## Pyang
- All types listed in `yang_type_specs`

## Ecosystem
### Yang
- [pyang](https://github.com/mbj4668/pyang): yang validator, transformator and code generator
- [libyang](https://github.com/CESNET/libyang): C-based yang parser
    - Only has [C++](https://github.com/CESNET/libyang-cpp/) and [Rust](https://github.com/rwestphal/yang2-rs/) bindings, but could become an option with some effort.
- [pyangbind](https://github.com/robshakir/pyangbind): extensive pyang plugin capable of generating python code (abandoned?)
    - Does its own parsing, storing and generating of YANG models. Possible starting off point if we don't find a library that does it for us.
- [ydk-gen](https://github.com/CiscoDevNet/ydk-gen)
- [yangson](https://github.com/CZ-NIC/yangson): python yang parser, editor
- [yang2swagger](https://github.com/bartoszm/yang2swagger): java cli tool
- [pyang-pydantic](https://github.com/karlnewell/pyang-pydantic): small, dodgy pyang plugin to generate pydantic files
- [jsontopydantic](https://github.com/brokenloop/jsontopydantic): Literally our entire project? Are we missing something?
### Restconf
- [pynso-restconf](https://github.com/workfloworchestrator/pynso-restconf)
- [restconf via requests example](https://github.com/twr14152/Network-Automation-Scripts_Python3/tree/master/restconf) [yang-python training examples](https://github.com/cmoberg/netconf-yang-training)

### Netconf
- [ncclient](https://github.com/ncclient/ncclient): python lib to make script interacting with netconf. Used in []()

## Utility
- [PDM Package Manager](https://pdm.fming.dev/)
- [Awesome Pyproject.toml](https://github.com/carlosperate/awesome-pyproject)

## Setup & Deployment
- Install
    - dependencies through pdm (`pdm install`)
        - into the local `__pypackages__` folder
            - to run your project as a python module
                - locally (`python -m yang2pydantic`)
                - in a docker container (see [Dockerfile](./Dockerfile))
            - to be accessed by your IDE for intellisense (see [.vscode/settings.json](./.vscode/settings.json))
            - to be accessed by your debug launch configuration (see [.vscode/launch.json](./.vscode/launch.json))
    - project through pip (`pip install .`)
        - to be used as a global CLI command (`run-my-project`)
- Build
    - through pdm (`pdm build`)
        - into the local `dist` folder
            - to be published on pypi
                - through twine (`twine upload dist/*`)
