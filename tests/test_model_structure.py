import ast
from typing_extensions import Self
from typing import List
from pydantic import validate_arguments
from pathlib import Path
import sys
import logging
from unittest.mock import patch

import pytest

LOGGER = logging.getLogger(__name__)


class ParsedAST:
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        with file.open() as f:
            self.ast = ast.parse(f.read())
        self.body: list[ast.stmt] = self.ast.body
        self.classes: dict[str, ast.ClassDef] = dict()
        for c in self.body:
            if isinstance(c, ast.ClassDef):
                bases = ", ".join([b.id for b in c.bases])
                self.classes[f'{c.name}({bases})'] = c

    @validate_arguments
    @staticmethod
    def assert_python_sources_equal(generated: Path, expected: Path):
        ast1 = ParsedAST(generated)
        ast2 = ParsedAST(expected)
        LOGGER.info(f'"Comparing:\n{"Expected":9}: {ast2.classes.keys()}\n{"Got":9}: {ast1.classes.keys()}')
        for a, b in zip(ast1.classes.keys(), ast2.classes.keys()):
            assert a == b, f'Missmatch {a} vs {b}\nGot: "{ast1.classes}"\nExpected: "{ast2.classes}"'
        for a, b in zip(ast1.classes.values(), ast2.classes.values()):
            # Compare classes
            assert len(a.body) == len(b.body)
            for a2, b2 in zip(a.body, b.body):
                # Compare class members
                annotation_a: ast.Name = getattr(a2, 'annotation', None)
                annotation_b: ast.Name = getattr(b2, 'annotation', None)
                # Compare annotation
                assert (annotation_a is None) == (annotation_b is None)
                if annotation_a is not None:
                    # Compare annotated type
                    assert getattr(annotation_a, 'id', None) == getattr(annotation_b, 'id', None)
        assert len(ast1.body) == len(ast2.body)


def run_pydantify(input_folder: Path, output_folder: Path, args: List[str] = []):
    model = input_folder / 'interfaces.yang'
    args = [
        sys.argv[0],
        *args,
        f'-i={input_folder}',
        f'-o={output_folder}',
        str(model),
    ]
    with patch.object(sys, 'argv', args):
        from pydantify.main import main

        try:
            main()
        except SystemExit:
            pass


@pytest.fixture(autouse=True)
def reset_optparse():
    from pyang import plugin

    # Reset plugins. Otherwise pyang creates cross-test side-effects. TODO: Better way?
    plugin.plugins = []


def test_minimal(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/minimal').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')


def test_minimal_trimmed(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/minimal').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=['-t=/interfaces/interfaces/address'],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected_trimmed.py')


def test_with_typedef(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/with_typedef').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')


def test_with_leafref(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/with_leafref').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')


def test_with_restrictions(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/with_restrictions').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')


def test_with_uses(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/with_uses').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')
