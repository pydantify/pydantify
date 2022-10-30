from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang.context import Context
from typing import Callable, List, Type

from pydantic.main import BaseModel

from ..models.models import NodeFactory
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser


# Helper function
def dynamically_serialized_helper_function():
    if 6 > 5:
        print("This is working.")


class ModelGenerator:
    @staticmethod
    def generate(ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        __class__.__generate(modules, fd)
        fd.write(__class__.__function_to_source_code(dynamically_serialized_helper_function))

    @staticmethod
    def __generate(modules: List[Statement], fd: TextIOWrapper):
        """Generates and yealds"""
        for module in modules:
            module: ModSubmodStatement
            mod = NodeFactory.generate(module)
            json = __class__.custom_dump(mod.to_pydantic_model())
            parser = JsonSchemaParser(
                json,
                snake_case_field=True,
                apply_default_values_for_required_fields=True,
                use_annotated=True,
                field_constraints=True,
                use_schema_description=True,
                reuse_model=True,
                strict_nullable=True,
            )
            result = parser.parse()
            fd.write(result)
            pass

    @staticmethod
    def custom_dump(model: Type[BaseModel]) -> str:
        schema = model.schema(by_alias=True)

        import json

        return json.dumps(schema)

    @staticmethod
    def __function_to_source_code(f: Callable):
        import inspect

        src = '\n\n'
        src += inspect.getsource(f)
        return src
