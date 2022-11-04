#!/usr/bin/env python

import json
from typing import List
import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    format='[%(levelname)s] %(pathname)s:%(lineno)d (%(funcName)s): %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger('pydantify')


def main():
    from .run import run
    from pathlib import Path

    # Parse user-give settings
    pyang_args = parse_cli_arguments()

    # Set sensible defaults
    pyang_args.append(f'--plugindir={Path(__file__).parent}/plugins')
    pyang_args.append('--format=pydantic')

    sys.argv[1:] = pyang_args

    run()


def parse_cli_arguments() -> List[str]:
    '''Parses and handles incoming CLI arguments and returns all the ones destined for Pydantic.'''
    import logging
    from argparse import ArgumentParser
    from .generator.model_generator import ModelGenerator

    # Setup parser
    parser = ArgumentParser(prog="pydantify", description='Transform a YANG model to a serializable Pydantic model.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose', help='Enables debug output', default=False
    )
    parser.add_argument(
        '-V',
        '--include-verification',
        action='store_true',
        dest='verify',
        help='Adds validation code to the output model.',
        default=False,
    )
    relay_args: List[str] = []

    # Parse
    args, unknown_args = parser.parse_known_args()

    # Apply known settings accordingly
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    ModelGenerator.include_verification_code = args.verify

    # Return args destined for pyang
    return list(set(unknown_args).union(relay_args))


if __name__ == "__main__":
    main()
