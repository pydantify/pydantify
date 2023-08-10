from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple, Type, TYPE_CHECKING, Optional
from datamodel_code_generator.reference import FieldNameResolver

from pyang.statements import (
    Statement,
)
from pyang.types import Decimal64Value
from pydantic import BaseConfig
from pydantic import BaseModel as PydanticBaseModel
from pydantic import create_model
from pydantic.fields import FieldInfo, Undefined, UndefinedType

from ..utility.yang_sources_tracker import YANGSourcesTracker

if TYPE_CHECKING:
    __class__: Type

logger = logging.getLogger("pydantify")


class BaseModel(PydanticBaseModel):
    # TODO[pydantic]: The `Config` class inherits from another class, please create the `model_config` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    class Config(BaseConfig):
        @staticmethod
        def schema_extra(schema: dict[str, Any], model: type[BaseModel]) -> None:  # type: ignore
            # Remove "title" property to avoid redundant annotation
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)
            if not schema.get("type", None) == "object":
                schema.pop("title", None)


@dataclass
class GeneratedClass:
    """Holds information about a dynamically generated output class."""

    class_name: str | UndefinedType = Undefined
    """Output class name"""
    cls: Type[BaseModel] | UndefinedType = Undefined
    """Ouput model class"""
    field_info: FieldInfo | UndefinedType = Undefined
    """Field info to add to field annotation"""
    field_annotation: Type | None = None
    """Annotated type when used """

    def assert_is_valid(self):
        for prop in self.__dataclass_fields__.keys():
            value = getattr(self, prop, Undefined)
            if value == Undefined:
                raise Exception(f'Member "{prop}" of class "{__class__.__name__}" is undefined.\n{self}')

    def to_field(self) -> Tuple[Type[BaseModel] | Type, FieldInfo]:
        # Exception if any field are Undefined
        self.assert_is_valid()
        return (
            self.field_annotation if self.field_annotation else self.cls,
            self.field_info,
        )  # type: ignore


class Node(ABC):
    _name_count: Dict[str, int] = dict()  # keeps track of the number of models with the same name
    alias_mapping: Dict[str, str] = dict()

    def __init__(self, stm: Statement):
        self.children: List[Node] = __class__.extract_statement_list(stm, "i_children")
        self.mandatory: bool = stm.search_one("mandatory", "true") or any(
            (ch for ch in self.children if ch.mandatory == True)
        )
        self.arg: str = stm.arg
        self.keyword: str = stm.keyword
        self.raw_statement: Statement = stm
        self.substmts: List[Statement] = stm.substmts
        self.comments: str | None = __class__.__extract_comments(stm)
        self.description: str | None = __class__.__extract_description(stm)

        default = getattr(self.raw_statement, "i_default", Undefined)
        if isinstance(default, Decimal64Value):
            self.default = default.value
        elif isinstance(default, Statement) and default.keyword == "identity":
            self.default = default.arg
        else:
            self.default = default
        self._name: Optional[str] = None

        self._output_model: GeneratedClass = GeneratedClass()
        YANGSourcesTracker.track_from_pos(stm.pos)

    def get_output_class(self) -> GeneratedClass:
        return self._output_model

    def get_qualified_name(self) -> str:
        qualified_name = f"{self.raw_statement.i_module.arg}:{self.arg}"
        self.alias_mapping[qualified_name] = FieldNameResolver(snake_case_field=True).get_valid_name(self.arg)
        return qualified_name

    @abstractmethod
    def name(self) -> str:
        pass

    def make_unique_name(self, suffix: str):
        if self._name is None:
            self._name = Node.ensure_unique_name(f"{self.arg.capitalize()}{suffix}")
        return self._name

    @classmethod
    def ensure_unique_name(cls, name: str) -> str:
        count: int = Node._name_count.setdefault(name, 0)
        ret: str = name
        if count > 0:
            ret = f"{name}{count+1}"
        Node._name_count[name] += 1
        return ret

    def get_base_class(self) -> type | Node | Enum:
        """Returns the class the output class should be derived from. Defaults to BaseModel."""
        return BaseModel

    @staticmethod
    def __extract_comments(stm: Statement) -> str | None:
        """Gathers and returns all comments located in the node's root, if present."""
        comments = stm.search("_comment")
        if comments:
            return " ".join((c.arg.lstrip("/ \n") for c in comments))
        return None

    @staticmethod
    def __extract_description(stm: Statement) -> str | None:
        """Returns the content of the "description" field, if present."""
        description = stm.search_one("description")
        return description.arg if description is not None else None

    def to_pydantic_model(self) -> Type[BaseModel]:
        """Generates the output class representing this node."""
        fields: Dict[str, Any] = self._children_to_fields()
        base = self.get_base_class()

        if isinstance(base, Node) or isinstance(base, Enum):
            raise Exception(f"Base model needs to be a class. Got {base}")

        output_model: Type[BaseModel] = create_model(self.name(), __base__=(base,), **fields)
        output_model.__doc__ = self.description or ""
        return output_model

    def _children_to_fields(self) -> Dict[str, Tuple[type, FieldInfo]]:
        ret: Dict[str, Tuple[type, FieldInfo]] = dict()
        for ch in self.children:
            ret[ch.arg] = ch._output_model.to_field()
        return ret

    @staticmethod
    def extract_statement_list(statement: Statement, attr_name: str) -> List[Node]:
        from .nodefactory import NodeFactory

        rv = getattr(statement, attr_name, [])
        return [ch for ch in map(NodeFactory.generate, rv) if ch is not None]
