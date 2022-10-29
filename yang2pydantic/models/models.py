from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Annotated, Any, Dict, List, Tuple, Type


from pyang.statements import (
    LeafLeaflistStatement,
    ModSubmodStatement,
    Statement,
)
from pydantic import BaseConfig, BaseModel as PydanticBaseModel, create_model
from pydantic.fields import FieldInfo, ModelField
from pydantic.types import constr


class BaseModel(PydanticBaseModel):
    class Config:
        # arbitrary_types_allowed = True
        pass


# https://network.developer.nokia.com/sr/learn/yang/understanding-yang/
# https://www.rfc-editor.org/rfc/rfc6020#section-7


class NotImplementedException(Exception):
    pass


@dataclass
class GeneratedClass:
    """Holds information about dynamically generated output plasses."""

    class_name: str
    cls: type
    field_info: FieldInfo


class Node(ABC):
    def __init__(self, stm: Statement):
        self.children: List[Type[Node]] = __class__.extract_statement_list(stm, 'i_children')
        self.arg: str = stm.arg
        self.keyword: str = stm.keyword
        self.raw_statement: Type[Statement] = stm
        self.substmts: List[Type[Statement]] = stm.substmts
        self.comments: str | None = __class__.__extract_comments(stm)
        self.description: str | None = __class__.__extract_description(stm)
        self.default = getattr(self.raw_statement, "i_default", None)

        self.__output_class: GeneratedClass = None

    @abstractmethod
    def get_output_class_name(self) -> str:
        """Returns the name of the output class."""
        pass

    def get_base_class(self) -> type:
        """Returns the class the output class should be derived from. Defaults to BaseModel."""
        return BaseModel

    @property
    def output_class(self) -> GeneratedClass:
        """Generates or fetches all the data necessary to integrate the node in the output model."""
        if self.__output_class is None:
            self.__output_class = GeneratedClass(
                class_name=self.get_output_class_name(),
                cls=self.to_pydantic_model(),
                field_info=self.to_pydantic_field(),
            )
        return self.__output_class

    @staticmethod
    def __extract_comments(stm: Statement) -> str | None:
        """Gathers and returns all comments located in the node's root, if present."""
        comments = stm.search('_comment')
        if comments:
            return " ".join((c.arg.lstrip('/ \n') for c in comments))
        return None

    @staticmethod
    def __extract_description(stm: Statement) -> str | None:
        """Returns the content of the "description" field, if present."""
        description = stm.search_one('description')
        return description.arg if description is not None else None

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        a = create_model(self.get_output_class_name(), __base__=self.get_base_class(), **fields)
        a.__doc__ = self.description
        return a

    @abstractmethod
    def to_pydantic_field(self) -> FieldInfo:
        pass

    def _children_to_fields(self) -> Dict[str, Tuple[Any]]:
        return {ch.arg: (ch.output_class.cls, ch.output_class.field_info) for ch in self.children}

    @staticmethod
    def extract_statement_list(statement: Statement, attr_name: str) -> List[Node]:
        rv = getattr(statement, attr_name, [])
        return [ch for ch in map(NodeFactory.generate, rv) if ch is not None]


class NodeFactory:
    # src: statements.data_definition_keywords
    @dataclass
    class ClassMapping:
        maps_to: type

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.maps_to(*args, **kwds)

    known_types: Dict[str, Type[Node]] = dict()
    _implemented_mappings: Dict[str, ClassMapping] = {}

    @classmethod
    def register_statement_class(cls, keywords: List[str]):
        for keyword in keywords:
            assert keyword not in cls._implemented_mappings.keys()

        def _register(type: type):
            for keyword in keywords:
                cls._implemented_mappings[keyword] = cls.ClassMapping(maps_to=type)

        return _register

    @classmethod
    def generate(cls, stm: Statement) -> Node:
        assert isinstance(stm, Statement)
        if stm.keyword not in cls._implemented_mappings.keys():
            raise Exception(f'"{stm.keyword}" has not yet been implemented as a type.')
        mapping = cls._implemented_mappings[stm.keyword]
        a = mapping.maps_to(stm)
        return a


@NodeFactory.register_statement_class(['leaf'])
class LeafNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        super().__init__(stm)
        pass

    def get_output_class_name(self) -> str:
        return f'{self.arg}Node'

    def get_base_class(self) -> type:
        return constr()  # TODO: different base class based on encountered type.

    def to_pydantic_field(self) -> FieldInfo:
        args = {}
        if self.default is not None:
            args['default'] = self.default
        return FieldInfo(**args)


@NodeFactory.register_statement_class(['module'])
class ModuleNode(Node):
    def __init__(self, module: ModSubmodStatement) -> None:
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module)

    def to_pydantic_field(self) -> FieldInfo:
        return None

    def get_output_class_name(self) -> str:
        return f"{self.arg}Module"
