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


@pytest.mark.parametrize(
    'input_dir,expected_file,args',
    [
        pytest.param('examples/minimal', 'examples/minimal/expected.py', [], id='minimal'),
        pytest.param(
            'examples/minimal',
            'examples/minimal/expected_trimmed.py',
            ['-t=/interfaces/interfaces/address'],
            id='minimal_trimmed',
        ),
        pytest.param('examples/with_typedef', 'examples/with_typedef/expected.py', [], id='typedef'),
        pytest.param('examples/with_leafref', 'examples/with_leafref/expected.py', [], id='leafref'),
        pytest.param('examples/with_restrictions', 'examples/with_restrictions/expected.py', [], id='restrictions'),
        pytest.param('examples/with_uses', 'examples/with_uses/expected.py', [], id='uses'),
    ],
)
def test_model(input_dir: str, expected_file: str, args: List[str], tmp_path: Path):
    input_folder = Path(__package__) / input_dir
    expected = Path(__package__) / expected_file
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=args,
    )
    ParsedAST.assert_python_sources_equal(tmp_path / 'out.py', expected)
