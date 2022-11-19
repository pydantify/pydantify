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
        self.classes: list[str] = [c.name for c in self.body if isinstance(c, ast.ClassDef)].sort()

    def __eq__(self, __o: Self) -> bool:
        assert self.__class__ == __o.__class__
        return len(self.body) == len(__o.body) and self.classes == __o.classes


@validate_arguments
def assert_python_sources_equal(f1: Path, f2: Path):
    ast1 = ParsedAST(f1)
    ast2 = ParsedAST(f2)
    assert ast1 == ast2


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
