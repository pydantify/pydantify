from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Type

from pyang.statements import (
    Statement,
)
from pydantic import BaseConfig
from pydantic import BaseModel as PydanticBaseModel
from pydantic import create_model
from pydantic.fields import FieldInfo, Undefined

from pydantify.models.yang_sources_tracker import YANGSourcesTracker

logger = logging.getLogger('pydantify')


class BaseModel(PydanticBaseModel):
    class Config(BaseConfig):
        # arbitrary_types_allowed = True
        pass

        @staticmethod
        def schema_extra(schema: dict[str, Any], model: type[BaseModel]) -> None:
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
            if not schema.get('type', None) == 'object':
                schema.pop('title', None)


@dataclass
class GeneratedClass:
    """Holds information about dynamically generated output plasses."""

    class_name: str = Undefined
    """Output class name"""
    cls: Type[BaseModel] = Undefined
    """Ouput model class"""
    field_info: FieldInfo = Undefined
    """Field info to add to field annotation"""
    field_annotation: Type | None = Undefined
    """Annotated type when used """

    def assert_is_valid(self):
        for prop in self.__dataclass_fields__.keys():
            value = getattr(self, prop, Undefined)
            if value == Undefined:
                raise Exception(f'Member "{prop}" of class "{__class__.__name__}" is undefined.\n{self}')

    def to_field(self) -> Tuple[Type[BaseModel] | Type, FieldInfo]:
        self.assert_is_valid()
        return (self.field_annotation if self.field_annotation else self.cls, self.field_info)


class Node(ABC):
    def __init__(self, stm: Statement):
        self.children: List[Type[Node]] = __class__.extract_statement_list(stm, 'i_children')
        self.arg: str = stm.arg
        self.keyword: str = stm.keyword
        self.raw_statement: Type[Statement] = stm
        self.substmts: List[Type[Statement]] = stm.substmts
        self.comments: str | None = __class__.__extract_comments(stm)
        self.description: str | None = __class__.__extract_description(stm)
        self.default = getattr(self.raw_statement, "i_default", Undefined)

        self.__output_class: GeneratedClass = GeneratedClass()
        YANGSourcesTracker.track_from_pos(stm.pos)

    def get_output_class(self) -> GeneratedClass:
        return self.__output_class

    @property
    def output_class_name(self):
        """Name of the output class."""
        return self.__output_class.class_name

    @output_class_name.setter
    def output_class_name(self, name: str):
        assert self.__output_class.class_name == Undefined
        self.__output_class.class_name = name

    @property
    def output_class_type(self):
        """Name of the output class."""
        return self.__output_class.cls

    @output_class_type.setter
    def output_class_type(self, cls: Type[BaseModel]):
        assert self.__output_class.cls == Undefined
        self.__output_class.cls = cls

    @property
    def output_field_info(self):
        """Name of the output class."""
        return self.__output_class.field_info

    @output_class_name.setter
    def output_field_info(self, field_info: FieldInfo):
        assert self.__output_class.field_info == Undefined
        self.__output_class.field_info = field_info

    @property
    def output_field_annotation(self):
        """Name of the output class."""
        return self.__output_class.field_annotation

    @output_field_annotation.setter
    def output_field_annotation(self, typ: type | None):
        assert self.__output_class.field_annotation == Undefined
        self.__output_class.field_annotation = typ

    def get_base_class(self) -> type:
        """Returns the class the output class should be derived from. Defaults to BaseModel."""
        return BaseModel

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
        base = self.get_base_class()
        output_model: Type[BaseModel] = create_model(self.output_class_name, __base__=(base,), **fields)
        output_model.__doc__ = self.description
        return output_model

    def _children_to_fields(self) -> Dict[str, Tuple[type, FieldInfo]]:
        ret: Dict[str, Tuple[type, FieldInfo]] = dict()
        for ch in self.children:
            ch: Node
            ret[ch.arg] = ch.__output_class.to_field()
        return ret

    @staticmethod
    def extract_statement_list(statement: Statement, attr_name: str) -> List[Type[Node]]:
        from pydantify.models.nodefactory import NodeFactory

        rv = getattr(statement, attr_name, [])
        return [ch for ch in map(NodeFactory.generate, rv) if ch is not None]
