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

from . import BaseModel, GeneratedClass, Node
from . import NodeFactory
from . import TypeResolver

logger = logging.getLogger("pydantify")


class Empty:
    pass


class TypeDefNode(Node):
    def __init__(self, stm: TypedefStatement) -> None:
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(
                self.default if self.default is not None or not self.mandatory else ...,
                alias=self.get_qualified_name(),
            ),
            cls=self.to_pydantic_model(),
        )

    def get_base_class(self) -> type:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def name(self) -> str:
        return self.make_unique_name(suffix="Type")

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this Typedef."""
        base_type = TypeResolver.resolve_statement(self.raw_statement)
        output_model: Type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **{}
        )
        output_model.__fields__["__root__"] = ModelField.infer(
            name="__root__",
            value=Undefined,
            annotation=base_type,
            class_validators={},
            config=BaseModel.Config,
        )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(["leaf"])
class LeafNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(
                self.default if self.default is not None or not self.mandatory else ...,
                description=self.description,
                alias=self.get_qualified_name(),
            ),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Leaf")

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
        output_model: Type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **fields
        )
        if base is not None:
            default = Undefined
            if base is Empty:  # TODO: ugly way of doing things
                base = str
                default = ""
            output_model.__fields__["__root__"] = ModelField.infer(
                name="__root__",
                value=default,
                annotation=base,
                class_validators={},
                config=BaseModel.Config,
            )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(["case"])
class CaseNode(Node):
    def __init__(self, stm: Statement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, Statement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(..., alias=self.get_qualified_name()),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Case")

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: Type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(["choice"])
class ChoiceNode(Node):
    def __init__(self, stm: ChoiceStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, ChoiceStatement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(
                ... if self.mandatory else None, alias=self.get_qualified_name()
            ),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Choice")

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        bases: tuple = tuple(x[0] for x in fields.values())
        output_model: Type[BaseModel] = Union[bases]
        return output_model


@NodeFactory.register_statement_class(["container"])
class ContainerNode(Node):
    def __init__(self, stm: ContainerStatement) -> None:
        logger.debug(f"Parsing {__class__.__name__}")
        assert isinstance(stm, ContainerStatement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=FieldInfo(
                ... if self.mandatory else None,
                alias=self.get_qualified_name(),
            ),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Container")


@NodeFactory.register_statement_class(["list"])
class ListNode(Node):
    def __init__(self, stm: ListStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, ListStatement)
        super().__init__(stm)

        output_class = self.to_pydantic_model()
        self._output_model = GeneratedClass(
            class_name=self.name(),
            cls=output_class,
            field_annotation=List[output_class],
            field_info=FieldInfo(..., alias=self.get_qualified_name()),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="ListEntry")

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: Type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = self.description
        return output_model


@NodeFactory.register_statement_class(["module"])
class ModuleNode(Node):
    def __init__(self, stm: ModSubmodStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, ModSubmodStatement)
        super().__init__(stm)

        output_class = self.to_pydantic_model()
        self._output_model = GeneratedClass(
            class_name=self.name(),
            cls=output_class,
            field_annotation=output_class,
            field_info=FieldInfo(...),
        )

    def to_pydantic_model(self) -> Type[BaseModel]:
        return super().to_pydantic_model()

    def name(self) -> str:
        return self.make_unique_name(suffix="Module")


class ModelRoot:
    def __init__(self, stm: Type[Statement]):
        self.root_node: Type[Node] = NodeFactory.generate(stm)

    def to_pydantic_model(self) -> Type[BaseModel]:
        fields: Dict
        if isinstance(self.root_node, ModuleNode):
            # Take only children, as
            fields = self.root_node._children_to_fields()
        else:
            fields = {self.root_node.arg: self.root_node.get_output_class().to_field()}
        output_model: Type[BaseModel] = create_model(
            "Model", __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = """
Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

## Tips
Initialization:
- all values have to be set via keyword arguments
- if a class contains only a `__root__` field, it can be initialized as follows:
    - `member=MyNode(__root__=<value>)`
    - `member=<value>`

Serialziation:
- `exclude_defaults=True` omits fields set to their default value (recommended)
- `by_alias=True` ensures qualified names are used (necessary)
"""
        return output_model
