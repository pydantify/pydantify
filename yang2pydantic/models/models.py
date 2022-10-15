from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Type
from pyang import statements
from pyang.context import Context
from pyang.statements import LeafLeaflistStatement, ModSubmodStatement, Statement, ContainerStatement, ListStatement, Statement, TypeStatement, TypedefStatement
from pyang.types import TypeSpec
from pydantic import BaseModel, Field, create_model
from pydantic.fields import Undefined


# https://network.developer.nokia.com/sr/learn/yang/understanding-yang/
# https://www.rfc-editor.org/rfc/rfc6020#section-7

class NotImplementedException(Exception):
    pass


class PyangStatement:
    def __init__(self, stm: Statement, *, resolve_substatements: bool = False, resolve_children: bool = False) -> None:
        assert isinstance(stm, Statement)
        # Print where the current data is coming from ASAP
        self._raw_statement: Statement = stm
        self.keyword = stm.keyword
        self.pos = stm.pos
        print(f'Creating "{self.keyword}" read from "{self.pos.ref}:{self.pos.line}"')

        # Load the rest of the values
        self.children = PyangStatement.extract_statement_list(stm, 'i_children') if resolve_children else []
        self.substmts = PyangStatement.extract_statement_list(stm, 'substmts') if resolve_substatements else []

        self.comments = " ".join((c.arg.lstrip('/ \n') for c in (stm.search('_comment'))))
        self.arg = stm.arg
        self.top = stm.top
        self.parent = stm.parent
        self.raw_keyword = stm.raw_keyword
        self.ext_mod = stm.ext_mod
        self.arg = stm.arg
        assert self.keyword == self.raw_keyword

    def to_pydantic_schema(self) -> Type[BaseModel]:
        return create_model(
            self.arg,
            __base__=BaseModel,
            **{}
        )

    def to_pydantic_field(self) -> Field:
        return Undefined

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
        a = cls._implemented_mappings[stm.keyword](stm)
        return a


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


class PyangModule(PyangStatement):
    def __init__(self, module: ModSubmodStatement) -> None:
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module, resolve_children=True, resolve_substatements=True)
        self.version: str = module.i_version
        self.prefix: str = module.i_prefix
        self.prefixes: Dict[str, Tuple[str, Any]] = module.i_prefixes
        self.unused_prefixes = module.i_unused_prefixes
        self.missing_prefixes = module.i_missing_prefixes
        self.modulename: str = module.i_modulename
        self.features = module.i_features
        self.identities: Dict[str, Statement] = module.i_identities
        self.extensions = module.i_extensions
        self.including_modulename = module.i_including_modulename
        self.ctx: Context = module.i_ctx
        self.undefined_augment_nodes = module.i_undefined_augment_nodes
        self.is_primary_module: bool = module.i_is_primary_module
        self.latest_revision: str = module.i_latest_revision

    def to_pydantic_schema(self) -> json:
        z = Annotated[str, Field(default="test", title="version")]
        k = ModelField(name="test", type_=z, default="123",required=False, class_validators={}, model_config=FieldConfig, )
        a = create_model(
            f"{self.arg}Module",
            __config__= FieldConfig,
            **{
                k.name: (k.type_, k.default)
            },
        )
        b = a.schema_json()
        return b


class FieldConfig(BaseConfig):
    arbitrary_types_allowed=True
