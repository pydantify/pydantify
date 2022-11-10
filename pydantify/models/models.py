from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import logging
from typing_extensions import Self

from typing import Any, Callable, Dict, List, Tuple, Type


from pyang.statements import (
    ContainerStatement,
    LeafLeaflistStatement,
    ListStatement,
    ModSubmodStatement,
    Statement,
)
from pydantic import BaseConfig, BaseModel as PydanticBaseModel, create_model
from pydantic.fields import FieldInfo, ModelField, Undefined
from pydantify.models.typeresolver import TypeResolver
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


# https://network.developer.nokia.com/sr/learn/yang/understanding-yang/
# https://www.rfc-editor.org/rfc/rfc6020#section-7


class NotImplementedException(Exception):
    pass


@dataclass
class GeneratedClass:
    """Holds information about dynamically generated output plasses."""

    class_name: str = Undefined
    cls: Type[BaseModel] = Undefined
    field_info: FieldInfo = Undefined
    field_annotation: Type | None = Undefined

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
        rv = getattr(statement, attr_name, [])
        return [ch for ch in map(NodeFactory.generate, rv) if ch is not None]


class NodeFactory:
    # src: statements.data_definition_keywords
    @dataclass
    class ClassMapping:
        maps_to: Callable[..., Type[Node]]

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.maps_to(*args, **kwds)

    known_types: Dict[str, Type[Node]] = dict()
    _implemented_mappings: Dict[str, ClassMapping] = {}

    @classmethod
    def register_statement_class(cls: Type[Self], keywords: List[str]):
        for keyword in keywords:
            assert keyword not in cls._implemented_mappings.keys()

        def _register(type: type):
            for keyword in keywords:
                cls._implemented_mappings[keyword] = cls.ClassMapping(maps_to=type)

        return _register

    @classmethod
    def generate(cls: Type[Self], stm: Type[Statement]) -> Type[Node]:
        assert isinstance(stm, Statement)
        known_model = TypeResolver.get_model_if_known(stm)
        if known_model is not None:
            return known_model
        else:
            if stm.keyword not in cls._implemented_mappings.keys():
                raise Exception(f'"{stm.keyword}" has not yet been implemented as a type.')
            mapping = cls._implemented_mappings[stm.keyword]
            node = mapping.maps_to(stm)
            TypeResolver.register(stm, node)
            return node


@NodeFactory.register_statement_class(['leaf'])
class LeafNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        super().__init__(stm)

        self.output_class_name = f'{self.arg.capitalize()}Leaf'
        self.output_field_annotation = None
        self.output_field_info = FieldInfo(self.default if self.default is not None else ...)
        self.output_class_type = self.to_pydantic_model()

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base = self.get_base_class()
        output_model: Type[BaseModel] = create_model(self.output_class_name, __base__=(BaseModel,), **fields)
        output_model.__fields__['__root__'] = ModelField.infer(
            name='__root__', value=Undefined, annotation=base, class_validators={}, config=BaseModel.Config
        )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['container'])
class ContainerNode(Node):
    def __init__(self, module: ContainerStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(module, ContainerStatement)
        super().__init__(module)

        self.output_class_name = f'{self.arg.capitalize()}Container'
        self.output_field_annotation = None
        self.output_field_info = FieldInfo(...)
        self.output_class_type = self.to_pydantic_model()


@NodeFactory.register_statement_class(['list'])
class ListNode(Node):
    def __init__(self, module: ListStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(module, ListStatement)
        super().__init__(module)

        self.output_class_name = f'{self.arg.capitalize()}ListEntry'
        self.output_class_type = self.to_pydantic_model()
        self.output_field_annotation = List[self.output_class_type]
        self.output_field_info = FieldInfo(...)

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        class_name = self.output_class_name
        output_model: Type[BaseModel] = create_model(class_name, __base__=(BaseModel,), **fields)
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['module'])
class ModuleNode(Node):
    def __init__(self, module: ModSubmodStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module)

        self.output_class_name = f'{self.arg.capitalize()}Module'
        self.output_class_type = self.to_pydantic_model()
        self.output_field_annotation = self.output_class_type
        self.output_field_info = FieldInfo(...)
        pass


class ModelRoot:
    def __init__(self, model: ModSubmodStatement):
        self.model: ModSubmodStatement = model
        self.module: ModuleNode = NodeFactory.generate(model)

    def to_pydantic_model(self) -> Type[BaseModel]:
        fields = {self.model.arg: self.module.get_output_class().to_field()}
        output_model: Type[BaseModel] = create_model('Model', __base__=(BaseModel,), **fields)
        return output_model
