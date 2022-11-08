from typing import Dict, Type, TYPE_CHECKING
from pyang.statements import Statement
from pyang.types import TypeSpec
from typing_extensions import Self

if TYPE_CHECKING:
    from pydantify.models.models import Node


class TypeResolver:
    __mapping: Dict[Type[Statement], Type['Node']] = dict()

    @classmethod
    def get_model_if_known(cls: Type[Self], stm: Type[Statement]) -> Type['Node'] | None:
        return TypeResolver.__mapping.get(stm, None)

    @classmethod
    def register(cls: Type[Self], stm: Type[Statement], model: Type['Node']):
        from pydantify.models.models import Node

        assert isinstance(model, Node) and isinstance(stm, Statement)
        cls.__mapping[stm] = model

    @classmethod
    def resolve_statement(cls: Type[Self], stm: Type[Statement]) -> type:
        # Check if already known
        ret = cls.__mapping.get(stm, None)
        if ret is not None:
            return ret

        # If not known, check type definition
        type = stm.search_one(keyword='type')
        typespec = getattr(type, 'i_type_spec', None)
        if typespec is not None:
            return cls.__resolve_type_spec(typespec)
        # If type is a typedef
        typedef = getattr(type, 'i_typedef', None)

        assert False  ## Not yet implemented

        base_type = None
        if typedef is not None:
            base_type = cls.resolve_statement(typedef)
            # TODO: Register type

    @classmethod
    def __resolve_type_spec(cls: Type[Self], spec: TypeSpec) -> Type:
        from pyang.types import (
            IntTypeSpec,
            BooleanTypeSpec,
            StringTypeSpec,
            PatternTypeSpec,
            PathTypeSpec,
            # TODO: Implement the following:
            TypeSpec,
            BitTypeSpec,
            BitsTypeSpec,
            EnumTypeSpec,
            EmptyTypeSpec,
            RangeTypeSpec,
            UnionTypeSpec,
            BinaryTypeSpec,
            LengthTypeSpec,
            LeafrefTypeSpec,
            IdentityrefTypeSpec,
            EnumerationTypeSpec,
            InstanceIdentifierTypeSpec,
        )

        from pydantify.models.models import NodeFactory

        match (spec.__class__.__qualname__):
            case PathTypeSpec.__qualname__:
                target_statement = getattr(spec, 'i_target_node')
                target = cls.get_model_if_known(target_statement)
                return target.output_class_type if target is not None else NodeFactory.generate(target_statement)
            case IntTypeSpec.__qualname__:
                return int
            case StringTypeSpec.__qualname__:
                return str
            case BooleanTypeSpec.__qualname__:
                return bool
            case PatternTypeSpec.__qualname__:
                return str  # TODO: constr()?
        assert False, 'Spec not yet implemented.'
