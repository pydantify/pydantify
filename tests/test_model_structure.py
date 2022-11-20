import ast
from typing_extensions import Self
from typing import List
from pydantic import validate_arguments
from pathlib import Path
import sys


class ParsedAST:
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        with file.open() as f:
            self.ast = ast.parse(f.read())
        self.body: list[ast.stmt] = self.ast.body
        self.classes: list[str] = []
        for c in self.body:
            if isinstance(c, ast.ClassDef):
                bases = ", ".join([b.id for b in c.bases])
                self.classes.append(f'{c.name}({bases})')
        self.classes.sort()


@validate_arguments
def assert_python_sources_equal(generated: Path, expected: Path):
    ast1 = ParsedAST(generated)
    ast2 = ParsedAST(expected)
    for a, b in zip(ast1.classes, ast2.classes):
        assert a == b, f'Missmatch {a} vs {b}\nGot: "{ast1.classes}"\nExpected: "{ast2.classes}"'
    assert len(ast1.body) == len(ast2.body), f'Got: "{ast1.body}"\nExpected: "{ast2.body}"'


def run_pydantify(input_folder: Path, output_folder: Path, args: List[str] = []):
    model = input_folder / 'interfaces.yang'
    args = [
        *args,
        f'-i={input_folder}',
        f'-o={output_folder}',
        str(model),
    ]
    sys.argv[1:] = args
    from pydantify.main import main

    try:
        main()
    except SystemExit:
        pass


def test_minimal(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/minimal').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')


def test_minimal_trimmed(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/minimal').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=['-t=/interfaces/interfaces/address'],
    )
    assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected_trimmed.py')


def test_with_typedef(tmp_path: Path):
    input_folder = Path(f'{__package__}/examples/with_typedef').absolute()
    run_pydantify(
        input_folder=input_folder,
        output_folder=tmp_path,
        args=[],
    )
    assert_python_sources_equal(tmp_path / 'out.py', input_folder / 'expected.py')
