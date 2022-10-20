from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang import statements
from pyang.context import Context
from typing import Dict, List
from ..models.models import PyangModule
from datamodel_code_generator import generate, InputFileType
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
            generate(json, snake_case_field=True, input_file_type=InputFileType.JsonSchema, output=Path('./out2.py'))
            pass
