from enum import Enum
from typing import Dict, List, Type, Optional, Union

from pyang.statements import Statement, TypedefStatement, TypeStatement
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
    Decimal64TypeSpec,
)
from pydantic import Field
from pydantic.types import conbytes, confloat, conint, constr
from pydantic_core import PydanticUndefinedType, core_schema
from typing_extensions import Annotated, Self

from . import Node
from ..utility.patterns import convert_pattern


class TypeResolver:
    __mapping: Dict[Statement, Node] = dict()

    @classmethod
    def get_model_if_known(cls: Type[Self], stm: Statement) -> Node | None:
        return TypeResolver.__mapping.get(stm, None)

    @classmethod
    def register(cls: Type[Self], stm: Statement, model: Node):
        assert isinstance(model, Node) and isinstance(stm, Statement)
        cls.__mapping[stm] = model

    @classmethod
    def resolve_statement(cls: Type[Self], stm: Statement) -> type | Node | Enum:
        # Check if already known
        ret: Optional[Node] = cls.__mapping.get(stm, None)
        if ret is not None:
            return ret

        # If not known, check type definition
        stm_type: TypeStatement = stm.search_one(keyword="type")

        # # If we need to deal with identity in a specific way:
        # if stm_type is None:
        #     if stm.keyword == "identity":
        #         return object
        #     raise NotImplementedError(f"Statement {stm} not implemented")

        return cls.__resolve_type_statement(stm_type=stm_type)

    @classmethod
    def __resolve_type_statement(
        cls: Type[Self], stm_type: TypeStatement
    ) -> type | Enum:
        typespec: TypeSpec = getattr(stm_type, "i_type_spec", None)
        typedef: TypedefStatement = getattr(stm_type, "i_typedef", None)

        if typedef is not None:  # Type is a typedef
            ret = cls.__mapping.get(typedef, None)
            if ret is None:
                from . import TypeDefNode

                typedef_node: Node = TypeDefNode(typedef)
                cls.register(typedef, typedef_node)
                output_type = typedef_node._output_model.cls
            else:
                output_type = ret._output_model.cls
            if isinstance(output_type, PydanticUndefinedType):
                raise Exception(f"{typedef_node} output model is Undefined")
            return output_type

        if typespec is not None:  # Type is a base type
            resolved = cls.__resolve_type_spec(typespec)
            return resolved

        assert False  ## Not yet implemented

    @classmethod
    def __resolve_type_spec(cls: Type[Self], spec: TypeSpec) -> type | Enum:
        from . import Node, NodeFactory

        match (spec.__class__.__qualname__):
            case RangeTypeSpec.__qualname__:
                if isinstance(spec.base, Decimal64TypeSpec):
                    spec.base.min = spec.min
                    spec.base.max = spec.max
                    return cls.__resolve_type_spec(spec.base)
                return conint(ge=spec.min, le=spec.max)
            case LengthTypeSpec.__qualname__:
                return constr(
                    min_length=spec.min,
                    max_length=spec.max,
                )
            case EnumTypeSpec.__qualname__:
                return Enum(
                    Node.ensure_unique_name(f"{spec.name}Enum"),
                    {x: x for x, _ in spec.enums},
                )  # TODO: make separate node type
            case PathTypeSpec.__qualname__:
                target_statement = getattr(spec, "i_target_node", None)

                if not target_statement:
                    """
                    Workaround until pyang supports leafref in Union
                    https://github.com/mbj4668/pyang/issues/724
                    """
                    from pyang.statements import v_reference_leaf_leafref

                    pyang_ctx = spec.i_source_stmt.top.i_ctx
                    stmt = spec.i_source_stmt.parent.parent.copy()
                    stmt.i_leafref = spec
                    stmt.i_leafref_expanded = False
                    v_reference_leaf_leafref(pyang_ctx, stmt)
                    target_statement = getattr(spec, "i_target_node", None)

                if cls.__mapping.get(target_statement, None) is None:
                    NodeFactory.generate(target_statement)
                node = cls.__mapping.get(target_statement)
                if isinstance(node, Node):
                    return node._output_model.cls  # type: ignore
            case IntTypeSpec.__qualname__:
                return conint(
                    ge=spec.min,
                    le=spec.max,
                )
            case Decimal64TypeSpec.__qualname__:
                # Workaround until pyang.type.Decimal64Value contains fd
                # prefered way: `spec.min.value * 10**-spec.min.fd`
                def conv_to_float(decimal_string: str):
                    if decimal_string.startswith("-."):
                        return float("-0" + decimal_string[1:])
                    if decimal_string.startswith(".-"):
                        return float("-0." + decimal_string[2:])
                    if decimal_string.startswith("."):
                        return float("0" + decimal_string)
                    return float(decimal_string)

                min_value = conv_to_float(spec.min.s)
                max_value = conv_to_float(spec.max.s)

                return confloat(
                    ge=min_value,
                    le=max_value,
                )
            case StringTypeSpec.__qualname__:
                return str
            case BooleanTypeSpec.__qualname__:
                return bool
            case BinaryTypeSpec.__qualname__:
                return conbytes(
                    min_length=spec.min,
                    max_length=spec.max,
                )
            case PatternTypeSpec.__qualname__:
                pattern = cls.__resolve_pattern(patterns=spec.res)
                return constr(pattern=convert_pattern(pattern))
            case EmptyTypeSpec.__qualname__:
                return dict
            case (
                IdentityrefTypeSpec.__qualname__
            ):  # TODO: abort before entering this stage?
                # def find_identityref(spec: IdentityrefTypeSpec):
                #     from pyang.util import prefix_to_module

                #     base_statement: BaseStatement = spec.idbases[0]
                #     base_arg: str = spec.idbases[0].arg
                #     module = base_statement.i_module
                #     pos = base_statement.pos
                #     errors = []

                #     prefix = None
                #     if ":" in base_arg:
                #         prefix, name = base_arg.split(":")
                #     else:
                #         name = base_arg

                #     if not prefix or prefix == module.i_module:
                #         prefix_module = module
                #     else:
                #         prefix_module = prefix_to_module(module, prefix, pos, errors)
                #         if prefix_module is None:
                #             raise Exception(f"No module found for prefix {prefix}")
                #     if stm := prefix_module.i_identities.get(name):
                #         return cls.resolve_statement(stm)
                #     raise Exception(f"No node {name} not found with prefix {prefix}")

                # return find_identityref(spec)
                return str
            case UnionTypeSpec.__qualname__:
                union = tuple([cls.__resolve_type_statement(typ) for typ in spec.types])
                return Union[union]  # type: ignore
            case BitTypeSpec.__qualname__:
                # Crafting a pattern like: ^(flag1|flag2|flag3|\s)*$
                pattern = "^(" + "|".join([b[0] for b in spec.bits]) + "|\\s)*$"
                return constr(pattern=pattern)
        assert False, f'Spec "{spec.__class__.__qualname__}" not yet implemented.'

    @classmethod
    def __resolve_pattern(cls, patterns: List[XSDPattern]) -> str:
        comnbined_pattern: str = "^"
        for pattern in patterns:
            pattern_spec: str = pattern.spec
            if not pattern_spec.startswith("^"):
                pattern_spec = "^" + pattern_spec
            if not pattern_spec.endswith("$"):
                pattern_spec += "$"
            comnbined_pattern += f"(?={pattern_spec})"
        return comnbined_pattern + ".*$"  # Capture everything if all lookaheads suceed
