from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Type

from pyang.statements import Statement
from pyang.types import (
    BooleanTypeSpec,
    EmptyTypeSpec,
    EnumTypeSpec,
    IntTypeSpec,
    LengthTypeSpec,
    PathTypeSpec,
    PatternTypeSpec,
    RangeTypeSpec,
    StringTypeSpec,
    TypeSpec,
    XSDPattern,
    # TODO: Implement the following:
    BinaryTypeSpec,
    BitsTypeSpec,
    BitTypeSpec,
    EnumerationTypeSpec,
    IdentityrefTypeSpec,
    InstanceIdentifierTypeSpec,
    LeafrefTypeSpec,
    UnionTypeSpec,
)
from pydantic.types import ConstrainedInt, conint, constr
from typing_extensions import Self

if TYPE_CHECKING:
    from . import Node


class TypeResolver:
    __mapping: Dict[Type[Statement], Type["Node"]] = dict()

    @classmethod
    def get_model_if_known(
        cls: Type[Self], stm: Type[Statement]
    ) -> Type["Node"] | None:
        return TypeResolver.__mapping.get(stm, None)

    @classmethod
    def register(cls: Type[Self], stm: Type[Statement], model: Type["Node"]):
        from . import Node

        assert isinstance(model, Node) and isinstance(stm, Statement)
        cls.__mapping[stm] = model

    @classmethod
    def resolve_statement(cls: Type[Self], stm: Type[Statement]) -> type:
        # Check if already known
        ret = cls.__mapping.get(stm, None)
        if ret is not None:
            return ret

        # If not known, check type definition
        type = stm.search_one(keyword="type")
        typespec = getattr(type, "i_type_spec", None)
        typedef = getattr(type, "i_typedef", None)

        if typedef is not None:  # Type is a typedef
            ret = cls.__mapping.get(typedef, None)
            if ret is None:
                from . import TypeDefNode

                ret = TypeDefNode(typedef)
                cls.register(typedef, ret)
            return ret

        if typespec is not None:  # Type is a base type
            resolved = cls.__resolve_type_spec(typespec)
            return resolved

        assert False  ## Not yet implemented

    @classmethod
    def __resolve_type_spec(cls: Type[Self], spec: TypeSpec) -> Type:
        from . import Node, NodeFactory, Empty

        match (spec.__class__.__qualname__):
            case RangeTypeSpec.__qualname__:
                base: ConstrainedInt = cls.__resolve_type_spec(spec.base)
                base.ge = spec.min
                base.le = spec.max
                return base
            case LengthTypeSpec.__qualname__:
                return constr(min_length=spec.min, max_length=spec.max)
            case EnumTypeSpec.__qualname__:
                base = Enum(
                    Node.ensure_unique_name(f"{spec.name}Enum"), dict(spec.enums)
                )  # TODO: make separate node type
                return base
            case PathTypeSpec.__qualname__:
                target_statement = getattr(spec, "i_target_node")
                if cls.__mapping.get(target_statement, None) is None:
                    NodeFactory.generate(target_statement)
                return cls.__mapping.get(target_statement)._output_model.cls
            case IntTypeSpec.__qualname__:
                return conint(ge=spec.min, le=spec.max)
            case StringTypeSpec.__qualname__:
                return str
            case BooleanTypeSpec.__qualname__:
                return bool
            case PatternTypeSpec.__qualname__:
                pattern = cls.__resolve_pattern(patterns=spec.res)
                return constr(regex=pattern)
            case EmptyTypeSpec.__qualname__:
                return Empty
            case IdentityrefTypeSpec.__qualname__:  # TODO: abort before entering this stage?
                return Empty
        assert False, f'Spec "{spec.__class__.__qualname__}" not yet implemented.'

    @classmethod
    def __resolve_pattern(cls, patterns: List[XSDPattern]):
        comnbined_pattern: str = "^"
        for pattern in patterns:
            pattern: str = pattern.spec
            if not pattern.startswith("^"):
                pattern = "^" + pattern
            if not pattern.endswith("$"):
                pattern += "$"
            comnbined_pattern += f"(?={pattern})"
        return comnbined_pattern + ".*$"  # Capture everything if all lookaheads suceed
