# pydantic

!!! note

    This text has been gratefully copied from the Term project documentation by D. Jovicic and D. Walther.

Pydantic is a data validation library for Python with some very appealing features:

- It can do runtime type-checking of arguments when instantiating classes or assigning to one of its member fields
- It allows even complex class structures with inheritance and compositions to be instantiated with a JSON-like dictionary
- It can serialize the content of a class to JSON, provided it consists only of python-native types or if custom serialization functions are provided for non-native types
- It can serialize and de-serialize a class structure, allowing it to be stored or sent as JSON
- It can do automatic type-casting and conversion between native types, allowing it to inter-operate with applications written in untyped languages, such as JavaScript
- Despite relying heavily on generic and dynamically generated classes, it provides a lot of type-hinting information to the IDE, making it easy to work with


These features are provided through a series of classes any developer should be familiar with when using pydantic for their project. The rest of this subsection aims to provide an overview of said classes and their purpose.


### BaseModel

The `BaseModel` class lies at the heart of every pydantic project. It is the base class each class needs to inherit from, if it wants to make use of the aforementioned pydantic features and become a *Pydantic Model*.

When a class inherits from `BaseModel`, it fundamentally changes how the class works. For instance, member fields are no longer declared in the `__init__()` method, instead needing to be declared directly in the class body like conventional static members. Type annotation also plays a crucial role, as pydantic tries to convert any input given during construction to the annotated type - if no type is provided or the provided type is unknown to pydantic (meaning it does not inherit from `BaseModel`, nor provide its own validator), an exception is raised by default. Additionally, such a class can automatically be instantiated from a dictionary of its fields, even without declaring an `__init__()` method explicitly.

The integration with Python's dictionary type does not end there however. Any class inheriting from `BaseModel` can be serialized to a schema-dictionary via the `.schema()` method. Any properties pertaining to the data of the class are preserved in said schema, such as field types, names, defaults and value constraints in a way that is compatible with **JSON Schema Core** and **OpenAPI**. Other class attributes such as methods, however, are not included, which is relevant when used in combination with the Datamodel Code Generator (DMCG).


### Config

Defining a `Config` class within a model adds the option of modifying model-wide settings. Some of the most widely used settings include ((pydantic docs)[https://docs.pydantic.dev/usage/model_config/#options]):


- `allow_mutation`: whether `__setattr__()` is allowed
- `arbitrary_types_allowed`: whether to allow arbitrary user types for fields (validation simply consists of checking if the type matches when enabled)
- `extra`: whether to ignore, allow, or forbid extra attributes during initialization
- `underscore_attrs_are_private`: whether to treat any underscore fields as private, or leave them as is
- `validate_assignment`: whether to perform validation on assignment to attributes


### Type Annotation and Validation

Input validation in pydantic is primarily declared via type-annotation.
Pydantic's validation supports numerous types and therefore will be summarized aggressively here. (A complete list of supported types can be found at https://pydantic-docs.helpmanual.io/usage/types/)

- Most native Python types are supported, including but not limited to: `bool`, `int`, `str`, `bytes`, `list`, `dict` and `tuple`.
- Various types of `enum` are supported.
- Various types found in the **ipaddress** library are supported for IP validation.
- Most types provided by the **typing** library are supported, including `Optional`, `Union`, `Sequence`, `Type`, `Callable`, `Pattern` and `Annotated`.
- Pydantic offers several additional *constrained types*, such as `stricturl`, `PositiveFloat`, `conint` and `constr`. Most of these are built upon other types, with additional customizable restrictions.
- If the supported types are not sufficient, custom ones can be added by creating classes that provide their own validators via a `__get_validators__()` method, even if they do not inherit from `BaseModel`.
