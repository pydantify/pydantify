# pyang

!!! note

    This text has been gratefully copied from the Term project documentation by D. Jovicic and D. Walther.


Pyang describes itself as "a YANG validator, transformator and code generator, written in Python". It is capable of translating YANG modules between various formats including YANG, YIN, DSDL, jsTree, among others. The library is extensible through plugins, most notably *PyangBind* and *pyang-pydantic*.


Being widely used in the industry while having released version 1.0 over 12 years ago *should* indicate that it is a fairly reliable tool. However, being that old comes at a cost: it maintains backwards compatibility all the way to Python 2.7. It does so by using only the subset of Python instructions valid in both Python 2.7 and 3.6, occasionally using branching code paths where necessary. It therefore comes with no type hints, f-strings, list comprehensions, match-case statements or any number of other features that have improved the legibility of Python code since the Python 2.7 release.


## Usage

Pyang is primarily designed to be used as a CLI tool, but it does offer a few additional options:


There are other options however:

- **Using Pyang as an intermediate translation step**
    - **pro:** this would expand our tool options. For example YIN (which is effectively XML) can be interpreted by off-the-shelve Python libraries, making it easier for us to parse.
    - **pro:** we would not need to concern ourselves with any of the Pyang internals.
    - **con:** on its own, this would require any YANG to pydantic conversion to be done in multiple steps (Eg. translating YANG to YIN using Pyang, then generating a pydantic model from said YIN output).
- **Using Pyang as a library**
    - **pro:** models could be used directly upon loading, without translating them to another format first. This could eliminate the need for an additional dependency in the chain.
    - **con:** as this is not the primary intended use-case, there is no intended interface for us to use, leading to increased coupling as we would need to access the library's internals directly.
- **Extending Pyang with a plugin of our own**
    - **pro:** it's the intended interface by which to add functionality to pyang, giving us greater guarantees that the components we would rely on will stay the same.
    - **con:** implemented this way, our project would effectively be a pure translator, running only when the user requires a model to be converted from one format to another. This would limit our ability to add functionality designed to aid the user after the initial conversion. For example, if the user intends to modify the pydantic schema we would likely not be able to offer any editing tools (Eg. pruning a branch of the model-tree would have to be done manually by the user). Any mistakes by the user would only be noticeable when attempting to convert the pydantic model back to a YANG module, requiring a trial-and-error approach.
    - **additional complication:** neither of us has prior experience writing extensions for third-party software, leading to more uncertainty in our estimates for potential risks and challenges.



## Pyang In-Depth

In this chapter, we will cover the pyang project in more detail, specifically the parts relevant to our project. It is by no means a comprehensive review, but it should serve as a crash-course for anyone improving upon or maintaining our project.


### The plugin system

Pyang can be extended at runtime through a fairly typical plugin interface. The `pyang` console-command supports a `--plugindir="<path>"` flag that, if present, prompts Pyang to look for additional plugins situated at the given path and import them through the [importlib](https://pypi.org/project/importlib/) library.

For Pyang to recognise a Python script as a valid plugin, it needs to contain a `pyang_plugin_init()` function. This function will be called by Pyang once it is ready to initialize plugins and must in turn call `register_plugin()` with an instance of a class which inherits from `PyangPlugin` as its argument. Said class must:


- Call the super-class' constructor with its own name as the argument.
- Implement `add_output_format(self, fmts)` to associate the plugin with a given output file format.
- Implement `emit(self, ctx, modules, fd)`, which gets called after Pyang has parsed a YANG model if the user requests the output to be in the associated format.


This shows a Pyang plugin with no additional functionality:

```python title="Barebones Pyang plugin"
from pyang.plugin import PyangPlugin, register_plugin
from pyang.statements import ModSubmodStatement
from pyang.context import Context
from typing import List, Dict


def pyang_plugin_init():
  register_plugin(MyPlugin())


class MyPlugin(PyangPlugin):
  def __init__(self):
    # Pass on the name of the plugin
    super().__init__(name="my-plugin-name")

  def add_output_format(self, fmts: Dict[str, PyangPlugin]):
    # Register self as the plugin in charge of "my-format" inputs
    fmts["my-format"] = self

  def emit(self, ctx: Context, modules: List[ModSubmodStatement], fd):
    # Main functionality goes here.
    # Once converted, write the output to the "fd" file-descriptor.
    pass
```


This approach works quite well, but it does come with a slight disadvantage, namely that the plugins folder can not contain any non-plugin files in order to avoid Pyang logging it as an error. This has slight implications on the project's structure, as it requires a separate folder just for the plugin's entry-point.

### Pyang classes

#### Statements

Statements represent most of the common YANG keywords such as `module`, `list`, `leaf`, `container`, `type`, etc. These are effectively the nodes in the YANG tree structure and are all derived from a common `Statement` class, often with very few additions.

`Statement` instances make heavy use of Python `__slots__`, which is effectively a whitelist of field names that are allowed within the instance. This means that, unlike conventional classes, arbitrary fields cannot be added to an instance at runtime. Additionally, the way these `__slots__` are used in Pyang leads to many of the fields being declared but not initialized, causing exceptions to be raised when accessed, even by an IDE. This, combined with YANG's heavy use of optional substatements can lead to situations in which the majority of a `Statement`'s fields are undefined. Direct access to fields therefore needs careful consideration.

The `Statement` class also offers most of the functionality required for tree traversal, including `search()` and `search_one()` to locate the statement's children and substatements by either their `keyword` or `arg` values along with `main_module()`, used to find the root module of the tree. To simplify navigation even further, each `Statement` contains a reference to its `parent`. For debugging and logging purposes, each `Statement` also contains a `pos` field, referencing the file and line number from which it was parsed - a welcome addition when working on cross-referential models split up across several files.

#### TypeSpecs

`TypeSpec` and its derived classes hold information about the underlying type of a node. They contain the base type (for example an integer, float or string) and the restrictions the value must adhere to to be considered valid. These restrictions typically consist of value ranges, length restrictions, regular expressions (called "patterns") or pre-defined values (called "enums").

These classes also contain a `validate()` function which, as the name implies, validates whether a given value matches the restrictions imposed on the type. Unfortunately for pydantify, these functions are tightly coupled to the Pyang project and cannot be easily repurposed for input validation in the output model.
