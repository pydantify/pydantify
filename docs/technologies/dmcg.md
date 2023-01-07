# datamodel-code-generator

!!! note

    This text has been gratefully copied from the Term project documentation by D. Jovicic and D. Walther.

Datamodel-code-generator (or DMCG for short) is a project which aims to translate data models written in either the ApenAPI 3 or JSONSchema format into Python class structures based on pydantic. While it is primarily designed as a CLI tool, it can easily be used as a library and integrated into other projects (though the lack of documentation surrounding this use-case requires some reverse-engineering).

Some notable features include:

- automatic generation of import statements based on the types and methods present in the schema being translated
- support for annotating classes via Python docstrings for ease of use within IDEs
- ability to re-use and reference other classes within the schema (meaning two classes containing a field of the same type do not lead to said type appearing twice in the output model)
- ability to rename classes and fields in order to not cause syntax errors, while still allowing initialization by the original name through pydantic's `alias` attribute


As of September 2022, datamodel-code-generator only supports pydantic V1, however the developer has been made aware of the impending V2 update in issue [#803](https://github.com/koxudaxi/datamodel-code-generator/issues/803).
