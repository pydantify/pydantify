from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang.context import Context
from typing import Callable, List, Type

from pydantic.main import BaseModel
from yang2pydantic.models.yang_sources_tracker import YANGSourcesTracker

from ..models.models import NodeFactory
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
import logging
from pathlib import Path


logger = logging.getLogger('pydantify')


# Helper function
def dynamically_serialized_helper_function():
    if __name__ == "__main__":
        # Demonstration purposes only. Not included in actual output.
        # To run: pdm run python out/out.py
        from pathlib import Path

        with open(Path(__file__).parent.joinpath("sample_data.json")) as fd:
            import json

            data = json.load(fd)
            print(f"Input: {data}")
            a = InterfacesModuleNode(**data)
            print("Instantiation successful!")
            output = a.json(exclude_defaults=True, by_alias=True)
            print(f"Output: {output}")
            assert json.loads(output) == data
            print("Serialization successful!")


def validate():
    pass


class ModelGenerator:
    """In charge of generating the output model"""

    include_verification_code: bool = False
    input_dir: Path
    output_dir: Path

    @classmethod
    def generate(cls, ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        """Generate and write output model to a given file descriptor."""
        cls.__generate(modules, fd)
        fd.write('\n\n')
        fd.write(cls.__function_content_to_source_code(dynamically_serialized_helper_function))
        if cls.include_verification_code:
            fd.write('\n\n')
            fd.write(cls.__function_to_source_code(validate))
            YANGSourcesTracker.copy_yang_files(input_root=cls.input_dir, output_dir=cls.output_dir)

    @classmethod
    def __generate(cls, modules: List[Statement], fd: TextIOWrapper):
        """Generates and yealds"""
        for module in modules:
            module: ModSubmodStatement
            mod = NodeFactory.generate(module)
            json = cls.custom_dump(mod.to_pydantic_model())
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
