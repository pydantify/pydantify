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

from pydantify.models.base import Node, BaseModel, GeneratedClass
from pydantify.models.nodefactory import NodeFactory

logger = logging.getLogger('pydantify')


class Empty:
    pass


class TypeDef(Node):
    def __init__(self, stm: TypedefStatement) -> None:
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(self.default if self.default is not None else ...),
            cls=self.to_pydantic_model(),
        )

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Type')
        return self._name

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this Typedef."""
        base_type = TypeResolver.resolve_statement(self.raw_statement)
        output_model: Type[BaseModel] = create_model(self.name(), __base__=(BaseModel,), **{})
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

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(
                self.default if self.default is not None else ...,
                description=self.description,
            ),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Leaf')
        return self._name

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base = self.get_base_class()
        if isinstance(base, Node):
            base: Node
            base = base._output_model.cls
        output_model: Type[BaseModel] = create_model(self.name(), __base__=(BaseModel,), **fields)
        if base is not None:
            default = Undefined
            if base is Empty:  # TODO: ugly way of doing things
                base = str
                default = ''
            output_model.__fields__['__root__'] = ModelField.infer(
                name='__root__', value=default, annotation=base, class_validators={}, config=BaseModel.Config
            )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['case'])
class ContainerNode(Node):
    def __init__(self, stm: Statement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(stm, Statement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(...),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Case')
        return self._name

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: Type[BaseModel] = create_model(self.name(), __base__=(BaseModel,), **fields)
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['choice'])
class ContainerNode(Node):
    def __init__(self, stm: ChoiceStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(stm, ChoiceStatement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(...),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Choice')
        return self._name

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base: type = self.get_base_class()
        bases = tuple(x[0] for x in fields.values())
        output_model: Type[BaseModel] = Union[bases]
        return output_model


@NodeFactory.register_statement_class(['container'])
class ContainerNode(Node):
    def __init__(self, module: ContainerStatement) -> None:
        logger.debug(f'Parsing {__class__.__name__}')
        assert isinstance(module, ContainerStatement)
        super().__init__(module)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(...),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Container')
        return self._name


@NodeFactory.register_statement_class(['list'])
class ListNode(Node):
    def __init__(self, module: ListStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(module, ListStatement)
        super().__init__(module)

        output_class = self.to_pydantic_model()
        self._output_model = GeneratedClass(
            class_name=self.name(),
            cls=output_class,
            field_annotation=List[output_class],
            field_info=FieldInfo(...),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}ListEntry')
        return self._name

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: Type[BaseModel] = create_model(self.name(), __base__=(BaseModel,), **fields)
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(['module'])
class ModuleNode(Node):
    def __init__(self, module: ModSubmodStatement) -> None:
        logger.debug(f'Parsing {__class__}')
        assert isinstance(module, ModSubmodStatement)
        super().__init__(module)

        output_class = self.to_pydantic_model()
        self._output_model = GeneratedClass(
            class_name=self.name(),
            cls=output_class,
            field_annotation=output_class,
            field_info=FieldInfo(...),
        )

    def name(self) -> str:
        if self._name is None:
            self._name = Node.ensure_unique_name(f'{self.arg.capitalize()}Module')
        return self._name


class ModelRoot:
    def __init__(self, model: Type[Statement]):
        self.model: Type[Statement] = model
        self.root_node: ModuleNode = NodeFactory.generate(model)

    def to_pydantic_model(self) -> Type[BaseModel]:
        fields = {self.model.arg: self.root_node.get_output_class().to_field()}
        output_model: Type[BaseModel] = create_model('Model', __base__=(BaseModel,), **fields)
        return output_model
