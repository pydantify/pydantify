from __future__ import annotations
from dataclasses import dataclass
import logging
from typing_extensions import Self

from typing import Any, Callable, Dict, List, Type


from pyang.statements import (
    Statement,
)
from pydantify.models.typeresolver import TypeResolver

from pydantify.models.base import Node

logger = logging.getLogger('pydantify')


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
