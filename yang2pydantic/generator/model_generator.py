from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang.context import Context
from typing import Callable, List, Type

from pydantic.main import BaseModel

from ..models.models import NodeFactory
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
import logging

logger = logging.getLogger('pydantify')


# Helper function
def dynamically_serialized_helper_function():
    if __name__ == "__main__":
        # Demonstration purposes only. Not included in actual output.
        # To run: pdm run python examples/minimal/out.py
        from pathlib import Path

        with open(Path(__file__).parent.joinpath("sample_data.json")) as fd:
            import json

            data = json.load(fd)
            a = InterfacesModuleNode(**data)
            print("Instantiation successful!")
            print(f"Output: {a.json()}")
            assert json.loads(a.json()) == data
            print("Serialization successful!")


def validate():
    pass


class ModelGenerator:
    include_verification_code: bool = False

    @staticmethod
    def generate(ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        __class__.__generate(modules, fd)
        fd.write('\n\n')
        fd.write(__class__.__function_content_to_source_code(dynamically_serialized_helper_function))
        if __class__.include_verification_code:
            fd.write('\n\n')
            fd.write(__class__.__function_to_source_code(validate))

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

        return inspect.getsource(f)

    @staticmethod
    def __function_content_to_source_code(f: Callable):
        import inspect

        src = inspect.getsourcelines(f)[0]
        import re

        indentation = re.compile('^([\t ]+)').findall(src[1])[0]
        return "".join(line.replace(indentation, '', 1) for line in src[1:])
