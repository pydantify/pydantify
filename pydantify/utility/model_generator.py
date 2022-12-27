import json
import logging
from io import TextIOWrapper
from pathlib import Path
import sys
from typing import List, Type, Optional

from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pyang.context import Context
from pyang.statements import ModSubmodStatement, Statement
from pydantic.main import BaseModel
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

            output = model.json(exclude_defaults=True, by_alias=True)
            print(f"{output=}")

            assert json.loads(output) == input
            print("Serialization successful!")


def model_init_code():  # pragma: no cover
    if __name__ == "__main__":
        model = Model(
            # <Initialize model here>
        )

        restconf_payload = model.json(exclude_defaults=True, by_alias=True, indent=2)

        print(f"Generated output: {restconf_payload}")


def custom_model_config():  # pragma: no cover
    from pydantic import BaseConfig, Extra

    BaseConfig.allow_population_by_field_name = True
    BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
    BaseConfig.extra = Extra.forbid


class ModelGenerator:
    """In charge of generating the output model"""

    include_verification_code: bool = False
    input_dir: Path
    output_dir: Path
    standalone: bool = False
    trim_path: Optional[str] = None

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

        fd.write(function_content_to_source_code(custom_model_config))
        fd.write("\n\n")

        # Add initialization helper-code
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
                        "    # from pydantify.utility import restconf_patch_request"
                        if not cls.standalone
                        else "",
                        "    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)",
                    ]
                )
            )
        YANGSourcesTracker.copy_yang_files(
            input_root=cls.input_dir, output_dir=cls.output_dir
        )

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
            json = cls.custom_dump(mod.to_pydantic_model())
            parser = JsonSchemaParser(
                json,
                snake_case_field=True,
                apply_default_values_for_required_fields=True,
                use_annotated=True,
                field_constraints=True,
                use_schema_description=True,
                use_field_description=True,
                aliases=Node.alias_mapping,
                reuse_model=False,  # Causes DCG to aggressively re-use "equivalent" classes, even if unrelated.
                strict_nullable=True,
            )
            result = parser.parse()
            fd.write(result)
            pass

    @classmethod
    def split_path(cls: Type[Self], path: str) -> List[str]:
        return [p for p in path.split("/") if p != ""]

    @classmethod
    def trim(
        cls: Type[Self], statement: Type[Statement], path: List[str]
    ) -> Type[Statement] | None:
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
    def custom_dump(cls: Type[Self], model: Type[BaseModel]) -> str:
        schema = model.schema(by_alias=True)
        return json.dumps(schema)
