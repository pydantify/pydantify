#!/usr/bin/env python

from typing import List
import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    format="[%(levelname)s] %(pathname)s:%(lineno)d (%(funcName)s): %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("pydantify")


def main():
    from pyang.scripts.pyang_tool import run

    # Parse user-give settings
    sys.argv[1:] = parse_cli_arguments()

    run()


def parse_cli_arguments() -> List[str]:
    """Parses and handles incoming CLI arguments and returns all the ones destined for Pydantic."""

    # Import locally to not clutter scope of caller
    import logging
    from argparse import ArgumentParser
    from .utility.model_generator import ModelGenerator
    from pathlib import Path
    import os

    # Setup parser
    parser = ArgumentParser(
        prog="pydantify",
        description="Transform a YANG model to a serializable Pydantic model.",
        epilog="NOTE: All unknown arguments will be passed to Pyang as-is and without guarantees.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Enables debug output",
        default=False,
    )
    parser.add_argument(
        "-V",
        "--include-verification",
        action="store_true",
        dest="verify",
        help="Adds validation code, as well as the relevant YANG files, to the output model.",
        default=False,
    )
    parser.add_argument(
        "-S",
        "--standalone",
        action="store_true",
        dest="standalone",
        help="Generated output model has no dependency on Pydantify. All required code is copied into the output model.",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        "--path",
        dest="input_dir",
        help="The directory that contains the YANG input model. Defaults to the input file's folder.",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help='The directory that should be used to store the output model. Defaults to "$CWD/out".',
        default=f"{os.getcwd()}/out/",
    )
    parser.add_argument(
        "-f",
        "--output-file",
        dest="output_file",
        help='The name of the output file. Defaults to "out.py" for Pydantic output or "out.json" for JSON schema output.',
        default=None,
    )
    parser.add_argument(
        "input_file",
        action="store",
        help="The YANG file containing the entrypoint to the model to evaluate.",
    )
    parser.add_argument(
        "-t",
        "--trim-path",
        dest="trim_path",
        help="Get only the specified branch of the whole tree.",
        default=None,
    )
    parser.add_argument(
        "-j",
        "--json-schema",
        action="store_true",
        dest="json_schema_output",
        help="Output JSON schema instead of Pydantic models",
        default=False,
    )
    relay_args: List[str] = []

    # Parse
    args, unknown_args = parser.parse_known_args()

    # Apply known settings accordingly
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    ModelGenerator.include_verification_code = args.verify
    ModelGenerator.standalone = args.standalone
    ModelGenerator.json_schema_output = args.json_schema_output
    default_output_file = "out.json" if args.json_schema_output else "out.py"

    input_dir = (
        Path(args.input_file).absolute().parent
        if args.input_dir is None
        else Path(args.input_dir).absolute()
    )
    ModelGenerator.input_dir = input_dir
    relay_args.append(f"--path={input_dir}")

    ModelGenerator.trim_path = args.trim_path

    output_dir = Path(args.output_dir).absolute()
    ModelGenerator.output_dir = output_dir
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if not exists
    if args.json_schema_output is False:
        with open(output_dir / "__init__.py", "a"):  # Create init file if not exists
            pass
    relay_args.append(
        f"--output={output_dir}/{args.output_file if args.output_file is not None else default_output_file}"
    )
    relay_args.append(f"--plugindir={Path(__file__).parent}/plugins")
    relay_args.append("--format=pydantic")

    # Order of arguments matters.
    return relay_args + unknown_args + [args.input_file]
