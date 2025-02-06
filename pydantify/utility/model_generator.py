import json
import logging
import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Dict, List, Type, Optional

from collections import defaultdict
from datamodel_code_generator.model import pydantic_v2
from datamodel_code_generator.parser.base import Result
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pyang.context import Context
from pyang.statements import ModSubmodStatement, Statement
from pydantic import BaseModel
from typing_extensions import Self

from ..models import ModelRoot, Node
from . import YANGSourcesTracker
from . import function_content_to_source_code, function_to_source_code
from ..utility import restconf_patch_request

logger = logging.getLogger("pydantify")


# Helper function
def dynamically_serialized_helper_function():  # pragma: no cover
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

            output = model.model_dump_json(exclude_defaults=True, by_alias=True)
            print(f"{output=}")

            assert json.loads(output) == input
            print("Serialization successful!")


def model_init_code():  # pragma: no cover
    if __name__ == "__main__":
        model = Model(
            # <Initialize model here>
        )

        restconf_payload = model.model_dump_json(
            exclude_defaults=True, by_alias=True, indent=2
        )

        print(f"Generated output: {restconf_payload}")


class ModelGenerator:
    """In charge of generating the output model"""

    include_verification_code: bool = False
    input_dir: Path
    output_dir: Path
    standalone: bool = False
    trim_path: Optional[str] = None
    json_schema_output: bool

    @classmethod
    def generate(
        cls: Type[Self],
        ctx: Context,
        modules: List[ModSubmodStatement],
        fd: TextIOWrapper,
    ):
        """Generate and write output model to a given file descriptor."""
        # Generate actual model
        cls.__generate(modules, fd)
        fd.write("\n\n")

        # Add initialization helper-code if Pydantic models generated
        if cls.json_schema_output is False:
            cls.__generate_helper_code(fd)

    @classmethod
    def __generate(
        cls: Type[Self], modules: List[ModSubmodStatement], fd: TextIOWrapper
    ):
        """Generates and yields"""

        for module in modules:
            if cls.trim_path is not None:
                split_path = cls.split_path(cls.trim_path)
                module = cls.trim(module, split_path)
            if module is None:
                logger.error("Invalid module. Exiting.")
                sys.exit(0)
            mod = ModelRoot(module)
            pydantic_model = mod.to_pydantic_model()
            if pydantic_model is None:
                continue
            schema = cls.custom_dump(pydantic_model)
            result = (
                json.dumps(schema, indent=2)
                if cls.json_schema_output is True
                else cls.__generate_pydantic(json.dumps(schema))
            )
            # Keep mypy happy
            if isinstance(result, str):
                fd.write(result)
            else:
                logger.warning(
                    f"Expected string but got {type(result)} whilst parsing JSON"
                )
            pass

    @staticmethod
    def __generate_pydantic(json: str) -> str | dict[tuple[str, ...], Result]:
        """Generates pydantic models"""
        extra_template_data: defaultdict[str, dict[str, Any]] = defaultdict(dict)
        extra_template_data["#all#"]["config"] = {}
        extra_template_data["#all#"]["config"]["regex_engine"] = '"python-re"'
        parser = JsonSchemaParser(
            json,
            data_model_type=pydantic_v2.BaseModel,
            data_model_root_type=pydantic_v2.RootModel,
            data_type_manager_type=pydantic_v2.DataTypeManager,
            data_model_field_type=pydantic_v2.DataModelField,
            snake_case_field=True,
            apply_default_values_for_required_fields=True,
            use_annotated=True,
            field_constraints=True,
            use_schema_description=True,
            use_field_description=True,
            aliases=Node.alias_mapping,
            reuse_model=False,  # Causes DCG to aggressively re-use "equivalent" classes, even if unrelated.
            strict_nullable=False,
            allow_population_by_field_name=True,
            allow_extra_fields=False,
            collapse_root_models=True,
            extra_template_data=extra_template_data,
        )
        return parser.parse()

    @classmethod
    def __generate_helper_code(cls: Type[Self], fd: TextIOWrapper) -> None:
        if cls.standalone:
            fd.write(function_to_source_code(restconf_patch_request))
            fd.write("\n\n")

        if cls.include_verification_code:
            fd.write(
                function_content_to_source_code(dynamically_serialized_helper_function)
            )
        else:
            fd.write(function_content_to_source_code(model_init_code))
            fd.write("\n")
            fd.write(
                "\n".join(
                    [
                        "    # Send config to network device:",
                        (
                            "    # from pydantify.utility import restconf_patch_request"
                            if not cls.standalone
                            else ""
                        ),
                        "    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)",
                    ]
                )
            )
        YANGSourcesTracker.copy_yang_files(
            input_root=cls.input_dir, output_dir=cls.output_dir
        )

    @classmethod
    def split_path(cls: Type[Self], path: str) -> List[str]:
        return [p for p in path.split("/") if p != ""]

    @classmethod
    def trim(
        cls: Type[Self], statement: Statement, path: List[str]
    ) -> Statement | None:
        arg, path = path[0], path[1:]
        if arg == statement.arg:
            while len(path) > 0:
                for child in statement.i_children:
                    if child.arg == path[0]:
                        statement = child
                        path = path[1:]
                        break
                else:
                    logger.warn(
                        f'Path element "{path[0]}" not found in "{statement.arg}\n'
                        f'Available: [{", ".join(ch.arg for ch in statement.i_children)}]'
                    )
                    return None
            return statement
        return None

    @classmethod
    def custom_dump(cls: Type[Self], model: Type[BaseModel]) -> Dict[str, Any]:
        return model.model_json_schema(by_alias=True)
