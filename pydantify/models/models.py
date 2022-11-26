from __future__ import annotations
import logging

from typing import Any, Dict, List, Type, Union


from pyang.statements import (
    ChoiceStatement,
    ContainerStatement,
    LeafLeaflistStatement,
    ListStatement,
    ModSubmodStatement,
    Statement,
    TypedefStatement,
)
from pydantic import create_model
from pydantic.fields import FieldInfo, ModelField, Undefined
from pydantify.models.typeresolver import TypeResolver

from pydantify.models.base import Node, BaseModel
from pydantify.models.nodefactory import NodeFactory

logger = logging.getLogger('pydantify')


class TypeDef(Node):
    def __init__(self, stm: TypedefStatement) -> None:
        super().__init__(stm)

        self.output_class_name = f'{self.arg.capitalize()}Type'
        self.output_field_annotation = None
        self.output_field_info = FieldInfo(self.default if self.default is not None else ...)
        self.output_class_type = self.to_pydantic_model()

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this Typedef."""
        base_type = TypeResolver.resolve_statement(self.raw_statement)
        output_model: Type[BaseModel] = create_model(self.output_class_name, __base__=(BaseModel,), **{})
        output_model.__fields__['__root__'] = ModelField.infer(
            name='__root__', value=Undefined, annotation=base_type, class_validators={}, config=BaseModel.Config
        )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['leaf'])
class LeafNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        super().__init__(stm)

        self.output_class_name = f'{self.arg.capitalize()}Leaf'
        self.output_field_annotation = None
        self.output_field_info = FieldInfo(
            self.default if self.default is not None else ...,
            description=self.description,
        )
        self.output_class_type = self.to_pydantic_model()

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base = self.get_base_class()
        if isinstance(base, Node):
            base: Node
            base = base.output_class_type
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
    def __init__(self, model: Type[Statement]):
        self.model: Type[Statement] = model
        self.root_node: ModuleNode = NodeFactory.generate(model)

    def to_pydantic_model(self) -> Type[BaseModel]:
        fields = {self.model.arg: self.root_node.get_output_class().to_field()}
        output_model: Type[BaseModel] = create_model('Model', __base__=(BaseModel,), **fields)
        return output_model
