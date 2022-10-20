from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang import statements
from pyang.context import Context
from semver import parse
from ..models.models import PyangModule
from datamodel_code_generator import generate, InputFileType
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pathlib import Path


class ModelGenerator:
    @staticmethod
    def generate(ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        ModelGenerator.__generate(modules, fd)

    @staticmethod
    def __generate(modules: List[Statement], fd: TextIOWrapper):
        """Generates and yealds"""
        for module in modules:
            module: ModSubmodStatement
            json = PyangModule(module).to_pydantic_schema()
            parser = JsonSchemaParser(json, snake_case_field=True)
            result = parser.parse()
            fd.write(result)
            pass
