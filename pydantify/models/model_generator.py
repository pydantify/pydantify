import inspect
import json
import logging
import re
from io import TextIOWrapper
from pathlib import Path
from typing import Callable, List, Type

from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pyang.context import Context
from pyang.statements import ModSubmodStatement, Statement
from pydantic.main import BaseModel
from typing_extensions import Self

from pydantify.models.yang_sources_tracker import YANGSourcesTracker

from .models import ModelRoot

logger = logging.getLogger('pydantify')


# Helper function
def dynamically_serialized_helper_function():
    if __name__ == "__main__":
        # Demonstration purposes only. Not included in actual output.
        # To run: pdm run python out/out.py
        from pathlib import Path

        with open(Path(__file__).parent.joinpath("sample_data.json")) as fd:
            import json

            input = json.load(fd)
            print(f"{input=}")
            model = Model(**input)
            print("Instantiation successful!")

            output = model.json(exclude_defaults=True, by_alias=True)
            print(f"{output=}")

            assert json.loads(output) == input
            print("Serialization successful!")


def custom_model_config():
    from pydantic import BaseConfig, Extra

    BaseConfig.allow_population_by_field_name = True
    BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
    BaseConfig.extra = Extra.forbid


def validate():
    pass


class ModelGenerator:
    """In charge of generating the output model"""

    include_verification_code: bool = False
    input_dir: Path = None
    output_dir: Path
    trim_path: str = None

    @classmethod
    def generate(cls: Type[Self], ctx: Context, modules: List[ModSubmodStatement], fd: TextIOWrapper):
        """Generate and write output model to a given file descriptor."""
        cls.__generate(modules, fd)
        fd.write('\n\n')

        fd.write(cls.__function_content_to_source_code(custom_model_config))
        fd.write('\n\n')

        if cls.include_verification_code:
            fd.write(cls.__function_content_to_source_code(dynamically_serialized_helper_function))
            # fd.write('\n\n')
            # fd.write(cls.__function_to_source_code(validate))
        YANGSourcesTracker.copy_yang_files(input_root=cls.input_dir, output_dir=cls.output_dir)

    @classmethod
    def __generate(cls: Type[Self], modules: List[ModSubmodStatement], fd: TextIOWrapper):
        """Generates and yields"""

        for module in modules:
            if cls.trim_path is not None:
                split_path = cls.split_path(cls.trim_path)
                module = cls.trim(module, split_path)
            assert module is not None
            mod = ModelRoot(module)
            json = cls.custom_dump(mod.to_pydantic_model())
            parser = JsonSchemaParser(
                json,
                snake_case_field=True,
                apply_default_values_for_required_fields=True,
                use_annotated=True,
                field_constraints=True,
                use_schema_description=True,
                use_field_description=True,
                reuse_model=False,  # Causes DCG to aggressively re-use "equivalent" classes, even if unrelated.
                strict_nullable=True,
            )
            result = parser.parse()
            fd.write(result)
            pass

    @classmethod
    def split_path(cls: Type[Self], path: str) -> List[str]:
        ret = path.split('/')
        if ret[0] == '':
            ret = ret[1:]
        return ret

    @classmethod
    def trim(cls: Type[Self], statement: Type[Statement], path: List[str]) -> Type[Statement]:
        if path:
            arg, path = path[0], path[1:]
            if arg == statement.arg:
                if path:
                    for child in statement.i_children:
                        child: Type[Statement]
                        child_statement = cls.trim(child, path)
                        if child_statement is not None:
                            return child_statement
                else:
                    return statement
        return None

    @classmethod
    def custom_dump(cls: Type[Self], model: Type[BaseModel]) -> str:
        schema = model.schema(by_alias=True)
        return json.dumps(schema)

    @staticmethod
    def __function_to_source_code(f: Callable):
        return inspect.getsource(f)

    @staticmethod
    def __function_content_to_source_code(f: Callable):
        src = inspect.getsourcelines(f)[0]
        indentation = re.compile('^([\t ]+)').findall(src[1])[0]
        return "".join(line.replace(indentation, '', 1) for line in src[1:])
