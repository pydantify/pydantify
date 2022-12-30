from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Type

from pyang.statements import Statement
from typing_extensions import Self
from pydantify.exceptions import NotImplementedException

from . import Node
from . import TypeResolver

logger = logging.getLogger("pydantify")


class NodeFactory:
    # src: statements.data_definition_keywords
    @dataclass
    class ClassMapping:
        maps_to: Callable[..., Node]

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.maps_to(*args, **kwds)

    _implemented_mappings: Dict[str, ClassMapping] = {}
    _ignored_types: List[str] = [
        "rpc",
        "notification",
    ]  #  TODO: potential extension to project?

    @classmethod
    def register_statement_class(cls: Type[Self], keywords: List[str]):
        for keyword in keywords:
            assert keyword not in cls._implemented_mappings.keys()

        def _register(type: type):
            for keyword in keywords:
                cls._implemented_mappings[keyword] = cls.ClassMapping(maps_to=type)
            return type

        return _register

    @classmethod
    def generate(cls: Type[Self], stm: Statement) -> Node | None:
        assert isinstance(stm, Statement)
        known_model = TypeResolver.get_model_if_known(stm)
        if known_model is not None:
            return known_model
        else:
            if stm.keyword in cls._ignored_types:
                return None
            if stm.keyword not in cls._implemented_mappings.keys():
                raise NotImplementedException(
                    f'"{stm.keyword}" has not yet been implemented as a type.'
                )
            mapping = cls._implemented_mappings[stm.keyword]
            node = mapping.maps_to(stm)
            TypeResolver.register(stm, node)
            return node
