from __future__ import annotations
from operator import truediv
from sre_parse import State

from typing import Annotated, Any, Dict, List, Optional, Tuple, Type

from pyang.context import Context
from pyang.statements import (
    ContainerStatement,
    LeafLeaflistStatement,
    ModSubmodStatement,
    Statement,
    TypedefStatement,
    TypeStatement,
)
from pyang.types import TypeSpec
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.class_validators import validator
from pydantic.config import Extra
from pydantic.fields import Field, ModelField
from pydantic.types import conint, constr

# https://network.developer.nokia.com/sr/learn/yang/understanding-yang/
# https://www.rfc-editor.org/rfc/rfc6020#section-7


class NotImplementedException(Exception):
    pass


class PyangStatement(BaseModel):

    _raw_statement: Annotated[Statement, Field(exclude=True)]
    arg: Annotated[str, Field(exclude=True)] = ''
    children: Annotated[List[PyangStatement|Type[PyangStatement]], Field(exclude=True)] = []

    def __init__(
        self,
        stm: Statement,
        *,
        resolve_substatements: bool = False,
        resolve_children: bool = False,
    ) -> None:
        assert isinstance(stm, Statement)
        # Print where the current data is coming from ASAP
        print(f'Creating "{stm.keyword}" read from "{stm.pos.ref}:{stm.pos.line}"')
        children=PyangStatement.extract_statement_list(stm, 'i_children') if resolve_children else []
        super().__init__(
            arg=stm.arg,
            _raw_statement=stm,
            children=children,
        )
        # self.pos: Annotated[Any, Field(exclude=True)] = stm.pos
        # print(f'Creating "{self.keyword}" read from "{self.pos.ref}:{self.pos.line}"')
        # Load the rest of the values
        # self.substmts: Annotated[PyangStatement, Field(exclude=True)] = PyangStatement.extract_statement_list(stm, 'substmts') if resolve_substatements else []
        # self.typedefs: Annotated[Dict[str, TypedefStatement], Field(exclude=True)] = stm.i_typedefs
        # self.comments = " ".join((c.arg.lstrip('/ \n') for c in (stm.search('_comment'))))

    class Config:
        arbitrary_types_allowed = True
        # extra = Extra.allow

    def to_pydantic_schema(self) -> Type[BaseModel]:
        return create_model(self.arg, __base__=BaseModel, **{})

    def to_pydantic_field(self) -> Any:
        pass

    @staticmethod
    def extract_statement_list(statement: Statement, attr_name: str) -> List[PyangStatement]:
        rv = getattr(statement, attr_name, [])
        return [ch for ch in map(PyangStatementFactory.generate, rv) if ch is not None]


class GenericStatement(PyangStatement):
    def __init__(self, stm: Statement) -> None:
        super().__init__(stm)


class PyangStatementFactory:
    # src: statements.data_definition_keywords
    class ClassMapping(BaseModel):
        is_container: bool = False
        maps_to: type

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.maps_to(*args, **kwds)

    known_types: Dict[str, Type[PyangStatement]] = dict()
    _implemented_mappings: Dict[str, ClassMapping] = {}

    @classmethod
    def register_statement_class(cls, keywords: List[str], is_container: bool = False):
        for keyword in keywords:
            assert keyword not in cls._implemented_mappings.keys()

        def _register(type: type):
            for keyword in keywords:
                cls._implemented_mappings[keyword] = cls.ClassMapping(maps_to=type, is_container=is_container)

        return _register

    @classmethod
    def generate(cls, stm: Statement) -> PyangStatement:
        assert isinstance(stm, Statement)
        if stm.keyword not in cls._implemented_mappings.keys():
            cls.register_statement_class([stm.keyword])(GenericStatement)
            print(f'"{stm.keyword}" has not yet been implemented as a type.')
        mapping = cls._implemented_mappings[stm.keyword]
        a = mapping.maps_to(stm)
        return a

    @staticmethod
    def register_type_definition(type_name: str, type: PyangType):
        if __class__.known_types.get(type_name, None) is None:
            __class__.known_types[type_name] = type
        else:
            raise Exception(f"Type already registered. Possible duplicate type name: '{type_name}'")


@PyangStatementFactory.register_statement_class(['type'])
class PyangType(PyangStatement):
    def __init__(self, stm: TypeStatement) -> None:
        # Can contain: description, type, default, referencem status, units
        assert isinstance(stm, TypeStatement)
        super().__init__(stm)
        self.type_spec: TypeSpec = stm.i_type_spec
        pass


@PyangStatementFactory.register_statement_class(['typedef'])
class PyangTypedef(PyangStatement):
    def __init__(self, stm: TypedefStatement) -> None:
        # Can contain:  default, description, reference, status, type, units
        assert isinstance(stm, TypedefStatement)
        super().__init__(stm)
        pass


@PyangStatementFactory.register_statement_class(['leaf'])
class PyangLeaf(PyangStatement):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        super().__init__(stm)
        a = stm.search_one(keyword='type')
        self.description: str = "\n".join((d.arg for d in stm.search(keyword='description')))
        self.substmts
        print(self.comments)
        pass


@PyangStatementFactory.register_statement_class(['container'], is_container=True)
class PyangContainer(PyangStatement):
    def __init__(self, stm: ContainerStatement) -> None:
        super().__init__(stm)
        pass


@PyangStatementFactory.register_statement_class(['list'], is_container=True)
class PyangList(PyangStatement):
    def __init__(self, stm: Statement) -> None:
        super().__init__(stm)
        pass


@PyangStatementFactory.register_statement_class(['leaf-list'])
class PyangLeafList(PyangStatement):
    def __init__(self, stm: Statement) -> None:
        super().__init__(stm)
        pass


class FieldConfig(BaseConfig):
    arbitrary_types_allowed = True


class PyangModule(PyangStatement):
    #typedefs: Annotated[Dict[str, TypedefStatement], Field(exclude=True)] = {}
    version: constr(regex='^1$') = '1'  # Only PYANG RFC 6020 supported for now.
    latest_revision: str = ''

    def __init__(self, module: ModSubmodStatement) -> None:
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module, resolve_children=True, resolve_substatements=True)
        # self.prefixes: Dict[str, Tuple[str, Any]] = module.i_prefixes
        # self.unused_prefixes = module.i_unused_prefixes
        # self.missing_prefixes = module.i_missing_prefixes
        # self.modulename: str = module.i_modulename
        # self.features = module.i_features
        # self.extensions = module.i_extensions
        # self.including_modulename = module.i_including_modulename
        # self.ctx: Context = module.i_ctx
        # self.undefined_augment_nodes = module.i_undefined_augment_nodes
        # self.is_primary_module: bool = module.i_is_primary_module
        #self.typedefs = module.i_typedefs
        self.version: constr(regex='^1$') = module.i_version  # Only PYANG RFC 6020 supported for now.
        self.latest_revision: str | None

    def create_model_field(self, name, value) -> ModelField:
        return ModelField(
            name=name,
            type_=type(value),
            default=value,
            required=False,
            class_validators={},
            model_config=FieldConfig,
        )

    def to_pydantic_schema(self) -> str:
        fields_ = self.__fields__  # .serializable.__fields__
        fields: Dict[str, Tuple[type, Any]] = dict()  # name : (type, default_value)
        for name in fields_.keys():
            default = self.__class__.__fields__[name].get_default()
            type = fields_[name].type_
            fields[name] = (type, default if default is not None else ...)
        a = create_model(f"{self.arg}Module", __config__=FieldConfig, **fields)
        b = a.schema_json()
        return b
