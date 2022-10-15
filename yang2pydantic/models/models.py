from __future__ import annotations

import json
from abc import abstractmethod
from typing import Any, Dict, List, Tuple, Type

from pyang.context import Context
from pyang.statements import (ContainerStatement, LeafLeaflistStatement,
                              ModSubmodStatement, Statement, TypedefStatement,
                              TypeStatement)
from pyang.types import TypeSpec
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.fields import ModelField

# https://network.developer.nokia.com/sr/learn/yang/understanding-yang/
# https://www.rfc-editor.org/rfc/rfc6020#section-7


class NotImplementedException(Exception):
    pass


class PyangStatement:
    def __init__(
        self,
        stm: Statement,
        *,
        resolve_substatements: bool = False,
        resolve_children: bool = False,
    ) -> None:
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


class FieldConfig(BaseConfig):
    arbitrary_types_allowed = True


class PyangModule(PyangStatement):
    class Serializable(BaseModel):
        version: str
        prefix: str
        # identities: Dict[str, Statement] = {}
        latest_revision: str | None = None
        children: List[PyangStatement] = []

        class Config(FieldConfig):
            pass

    def __init__(self, module: ModSubmodStatement) -> None:
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module, resolve_children=True, resolve_substatements=True)
        self.prefixes: Dict[str, Tuple[str, Any]] = module.i_prefixes
        self.unused_prefixes = module.i_unused_prefixes
        self.missing_prefixes = module.i_missing_prefixes
        self.modulename: str = module.i_modulename
        self.features = module.i_features
        self.extensions = module.i_extensions
        self.including_modulename = module.i_including_modulename
        self.ctx: Context = module.i_ctx
        self.undefined_augment_nodes = module.i_undefined_augment_nodes
        self.is_primary_module: bool = module.i_is_primary_module
        self.serializable = __class__.Serializable(
            version=module.i_version,
            prefix=module.i_prefix,
            latest_revision=module.i_latest_revision,
            children=self.children,
            # identities=module.i_identities,
        )

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
        fields_ = self.serializable.__fields__
        fields: Dict[str, Tuple[Type, Any]] = {
            name: (fields_[name].type_, getattr(self.serializable, name, None))
            for name in fields_.keys()
        }
        a = create_model(f"{self.arg}Module", __config__=FieldConfig, **fields)
        b = a.schema()
        return json.dumps(b)
