from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, List, Union, TYPE_CHECKING

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
from pydantic.fields import Field

from . import BaseModel, GeneratedClass, Node, RootModel
from . import NodeFactory
from . import TypeResolver

if TYPE_CHECKING:
    __class__: type

logger = logging.getLogger("pydantify")


class TypeDefNode(Node):
    def __init__(self, stm: TypedefStatement) -> None:
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=Field(
                self.default if self.default is not None or not self.mandatory else ...,
                alias=self.get_qualified_name(),
            ),  # type: ignore[arg-type]
            cls=self.to_pydantic_model(),
        )

    def get_base_class(self) -> type | Node | Enum:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def name(self) -> str:
        return self.make_unique_name(suffix="Type")

    def to_pydantic_model(self) -> type[RootModel]:
        """Generates the output class representing this Typedef."""
        base_type = TypeResolver.resolve_statement(self.raw_statement)
        output_model: type[RootModel] = create_model(
            self.name(), __base__=(RootModel[base_type],)  # type: ignore[misc]
        )
        output_model.__doc__ = self.description or ""
        return output_model


@NodeFactory.register_statement_class(["leaf"])
class LeafNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=Field(
                self.default if self.default is not None or not self.mandatory else ...,
                description=self.description,
                alias=self.get_qualified_name(),
            ),  # type: ignore[arg-type]
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Leaf")

    def get_base_class(self) -> type | Node | Enum:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> type[BaseModel | RootModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base: Any = self.get_base_class()

        if isinstance(base, Node):
            base = base._output_model.cls

        output_model: type[BaseModel] | type[RootModel]
        if base is not None:
            output_model = create_model(
                self.name(), __base__=(RootModel[base],)  # type: ignore[misc]
            )
        else:
            output_model = create_model(self.name(), __base__=(BaseModel,), **fields)
        output_model.__doc__ = self.description or ""
        return output_model


@NodeFactory.register_statement_class(["case"])
class CaseNode(Node):
    def __init__(self, stm: Statement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, Statement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=Field(..., alias=self.get_qualified_name()),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Case")

    def to_pydantic_model(self) -> type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = self.description or ""
        return output_model


@NodeFactory.register_statement_class(["choice"])
class ChoiceNode(Node):
    def __init__(self, stm: ChoiceStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        assert isinstance(stm, ChoiceStatement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=Field(  # type: ignore[arg-type]
                ... if self.mandatory else None, alias=self.get_qualified_name()
            ),
            cls=self.to_pydantic_model(),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="Choice")

    def to_pydantic_model(self) -> type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        bases: tuple = tuple(x[0] for x in fields.values())
        output_model: type[BaseModel] = Union[bases]  # type: ignore
        return output_model


@NodeFactory.register_statement_class(["container"])
class ContainerNode(Node):
    def __init__(self, stm: ContainerStatement) -> None:
        logger.debug(f"Parsing {__class__.__name__}")
        assert isinstance(stm, ContainerStatement)
        super().__init__(stm)

        self._output_model = GeneratedClass(
            class_name=self.name(),
            field_info=Field(  # type: ignore[arg-type]
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
            field_annotation=List[output_class],  # type: ignore
            field_info=Field(  # type: ignore[arg-type]
                ... if self.mandatory else None, alias=self.get_qualified_name()
            ),
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="ListEntry")

    def to_pydantic_model(self) -> type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        output_model: type[BaseModel] = create_model(
            self.name(), __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = self.description or ""
        return output_model


@NodeFactory.register_statement_class(["leaf-list"])
class LeafListNode(Node):
    def __init__(self, stm: LeafLeaflistStatement) -> None:
        logger.debug(f"Parsing {__class__}")
        super().__init__(stm)

        output_class = self.to_pydantic_model()
        self._output_model = GeneratedClass(
            class_name=self.name(),
            cls=output_class,
            field_annotation=List[output_class],  # type: ignore
            field_info=Field(
                self.default if self.default is not None or not self.mandatory else ...,
                description=self.description,
                alias=self.get_qualified_name(),
            ),  # type: ignore[arg-type]
        )

    def name(self) -> str:
        return self.make_unique_name(suffix="LeafList")

    def get_base_class(self) -> type | Node | Enum:
        base = TypeResolver.resolve_statement(self.raw_statement)
        return base

    def to_pydantic_model(self) -> type[BaseModel | RootModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base: Any = self.get_base_class()

        if isinstance(base, Node):
            base = base._output_model.cls

        output_model: type[BaseModel] | type[RootModel]
        if base is not None:
            output_model = create_model(
                self.name(), __base__=(RootModel[base],)  # type: ignore[misc]
            )
        else:
            output_model = create_model(self.name(), __base__=(BaseModel,), **fields)
        output_model.__doc__ = self.description or ""
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
            field_info=Field(...),
        )

    def to_pydantic_model(self) -> type[BaseModel] | type[RootModel]:
        return super().to_pydantic_model()

    def name(self) -> str:
        return self.make_unique_name(suffix="Module")


class ModelRoot:
    def __init__(self, stm: type[Statement]):
        self.root_node: Node | None = NodeFactory.generate(stm)

    def to_pydantic_model(self) -> type[BaseModel] | None:
        fields: Dict
        if isinstance(self.root_node, ModuleNode):
            # Take only children, as
            fields = self.root_node._children_to_fields()
        elif isinstance(self.root_node, Node):
            fields = {self.root_node.arg: self.root_node.get_output_class().to_field()}
        output_model: type[BaseModel] = create_model(
            "Model", __base__=(BaseModel,), **fields
        )
        output_model.__doc__ = """
Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

## Tips
Initialization:
- all values have to be set via keyword arguments
- if a class contains only a `root` field, it can be initialized as follows:
    - `member=MyNode(root=<value>)`
    - `member=<value>`

Serialziation:
- `exclude_defaults=True` omits fields set to their default value (recommended)
- `by_alias=True` ensures qualified names are used (necessary)
"""
        return output_model if fields else None
