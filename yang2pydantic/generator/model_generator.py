from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang import statements
from pyang.context import Context
from typing import Callable, Dict, List

from semver import parse
from ..models.models import ModuleNode
from datamodel_code_generator import generate, InputFileType
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pathlib import Path


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
            mod = ModuleNode(module)
            json = mod.to_pydantic_model().schema_json()
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
    def __function_to_source_code(f: Callable):
        import inspect

        src = '\n\n'
        src += inspect.getsource(f)
        return src
