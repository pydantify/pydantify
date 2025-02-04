import ast
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, List
from unittest.mock import patch

import pytest
from pydantic import validate_call
from pytest import param
from typing_extensions import Self

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
                try:
                    bases = ", ".join([b.id for b in c.bases])  # type: ignore[attr-defined]
                except AttributeError:
                    bases = ", ".join([b.value.id for b in c.bases])  # type: ignore[attr-defined]
                self.classes[f"{c.name}({bases})"] = c

    @staticmethod
    def get_annotation(annotation: Any) -> ast.expr:
        return annotation.value if isinstance(annotation, ast.Subscript) else annotation

    @staticmethod
    @validate_call
    def assert_python_sources_equal(generated: Path, expected: Path):
        LOGGER.info(f"Output path: {generated}")
        ast1 = ParsedAST(generated)
        ast2 = ParsedAST(expected)
        LOGGER.info(
            f'"Comparing:\n{"Expected":9}: {ast2.classes.keys()}\n{"Got":9}: {ast1.classes.keys()}'
        )
        for c1, c2 in zip(ast1.classes.keys(), ast2.classes.keys()):
            assert (
                c1 == c2
            ), f'Mismatch {c1} vs {c2}\nGot: "{ast1.classes}"\nExpected: "{ast2.classes}"'
        for a, b in zip(ast1.classes.values(), ast2.classes.values()):
            # Compare classes
            assert len(a.body) == len(b.body)
            for a2, b2 in zip(a.body, b.body):
                # Compare class members
                annotation_a = getattr(a2, "annotation", None)
                annotation_b = getattr(b2, "annotation", None)
                # Compare annotation
                assert (annotation_a is None) == (annotation_b is None)
                if annotation_a is not None:
                    # Compare annotated type
                    assert getattr(
                        ast1.get_annotation(annotation_a), "id", None
                    ) == getattr(ast2.get_annotation(annotation_b), "id", None)
        assert len(ast1.body) == len(ast2.body)


def run_pydantify(input_file: Path, output_folder: Path, args: List[str] = []):
    args = [
        sys.argv[0],
        *args,
        f"-i={input_file.parent}",
        f"-o={output_folder}",
        str(input_file),
    ]
    with patch.object(sys, "argv", args):
        from pydantify.main import main

        try:
            main()
        except SystemExit as e:
            assert e.code == 0, f"Pyang exited with errors:\n{e}"


@pytest.fixture(autouse=True)
def reset_optparse():
    from pyang import plugin
    from pydantify.models.base import Node

    # Reset plugins. Otherwise pyang creates cross-test side-effects. TODO: Better way?
    plugin.plugins = []
    Node._name_count = dict()


@pytest.mark.parametrize(
    ("input_dir", "expected_file", "args"),
    [
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected.py",
            [],
            id="minimal",
        ),
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected_trimmed.py",
            ["-t=/interfaces/interfaces/address"],
            id="minimal_trimmed",
        ),
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected_standalone.py",
            ["--standalone"],
            id="minimal_standalone",
        ),
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected_trimmed.py",
            ["-t=interfaces/interfaces/address"],
            id="minimal_trimmed without leading /",
        ),
        param(
            "examples/with_typedef/interfaces.yang",
            "examples/with_typedef/expected.py",
            [],
            id="typedef",
        ),
        param(
            "examples/with_leafref/interfaces.yang",
            "examples/with_leafref/expected.py",
            [],
            id="leafref",
        ),
        param(
            "examples/with_restrictions/interfaces.yang",
            "examples/with_restrictions/expected.py",
            [],
            id="restrictions",
        ),
        param(
            "examples/with_uses/interfaces.yang",
            "examples/with_uses/expected.py",
            [],
            id="uses",
        ),
        param(
            "examples/with_case/interfaces.yang",
            "examples/with_case/expected.py",
            [],
            id="case",
        ),
        param(
            "examples/with_complex_case/interfaces.yang",
            "examples/with_complex_case/expected.py",
            [],
            id="complex case",
        ),
        param(
            "examples/turing-machine/turing-machine.yang",
            "examples/turing-machine/expected.py",
            [],
            id="turing machine",
        ),
        param(
            "examples/openconfig/openconfig-interfaces.yang",
            "examples/openconfig/expected.py",
            [
                "-t=openconfig-interfaces/interfaces/interface/config",
            ],
            id="openconfig",
        ),
        param(
            "examples/with_leaflist/interfaces.yang",
            "examples/with_leaflist/expected.py",
            [],
            id="leaf-list",
        ),
        param(
            "examples/with_union/interfaces.yang",
            "examples/with_union/expected.py",
            [],
            id="type union",
        ),
        param(
            "examples/with_identity_default/interfaces.yang",
            "examples/with_identity_default/expected.py",
            [],
            id="identity default",
        ),
        param(
            "examples/with_enum/interfaces.yang",
            "examples/with_enum/expected.py",
            [],
            id="enum",
        ),
        param(
            "examples/with_decimal64/interfaces.yang",
            "examples/with_decimal64/expected.py",
            [],
            id="decimal64",
        ),
        param(
            "examples/with_bits/interfaces.yang",
            "examples/with_bits/expected.py",
            [],
            id="bits",
        ),
        param(
            "examples/with_leafref2/keychains.yang",
            "examples/with_leafref2/expected.py",
            [],
            id="leafref2",
        ),
        param(
            "examples/with_identity_default_list/ciphers.yang",
            "examples/with_identity_default_list/expected.py",
            [],
            id="identity default list",
        ),
    ],
)
def test_model(input_dir: str, expected_file: str, args: List[str], tmp_path: Path):
    input_folder = Path(__package__) / input_dir
    expected = Path(__package__) / expected_file
    run_pydantify(
        input_file=input_folder,
        output_folder=tmp_path,
        args=args,
    )
    print("Temp file: " + str(tmp_path / "out.py"))
    ParsedAST.assert_python_sources_equal(tmp_path / "out.py", expected)


@pytest.mark.parametrize(
    ("input_dir", "expected_file", "args"),
    [
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected.json",
            ["-j"],
            id="minimal",
        ),
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected_trimmed.json",
            ["-j", "-t=/interfaces/interfaces/address"],
            id="minimal_trimmed",
        ),
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/expected_trimmed.json",
            ["-j", "-t=interfaces/interfaces/address"],
            id="minimal_trimmed without leading /",
        ),
        param(
            "examples/with_typedef/interfaces.yang",
            "examples/with_typedef/expected.json",
            ["-j"],
            id="typedef",
        ),
        param(
            "examples/with_leafref/interfaces.yang",
            "examples/with_leafref/expected.json",
            ["-j"],
            id="leafref",
        ),
        param(
            "examples/with_restrictions/interfaces.yang",
            "examples/with_restrictions/expected.json",
            ["-j"],
            id="restrictions",
        ),
        param(
            "examples/with_uses/interfaces.yang",
            "examples/with_uses/expected.json",
            ["-j"],
            id="uses",
        ),
        param(
            "examples/with_case/interfaces.yang",
            "examples/with_case/expected.json",
            ["-j"],
            id="case",
        ),
        param(
            "examples/with_complex_case/interfaces.yang",
            "examples/with_complex_case/expected.json",
            ["-j"],
            id="complex case",
        ),
        param(
            "examples/turing-machine/turing-machine.yang",
            "examples/turing-machine/expected.json",
            ["-j"],
            id="turing machine",
        ),
        param(
            "examples/openconfig/openconfig-interfaces.yang",
            "examples/openconfig/expected.json",
            [
                "-j",
                "-t=openconfig-interfaces/interfaces/interface/config",
            ],
            id="openconfig",
        ),
        param(
            "examples/with_leaflist/interfaces.yang",
            "examples/with_leaflist/expected.json",
            ["-j"],
            id="leaf-list",
        ),
        param(
            "examples/with_union/interfaces.yang",
            "examples/with_union/expected.json",
            ["-j"],
            id="type union",
        ),
        param(
            "examples/with_identity_default/interfaces.yang",
            "examples/with_identity_default/expected.json",
            ["-j"],
            id="identity default",
        ),
        param(
            "examples/with_enum/interfaces.yang",
            "examples/with_enum/expected.json",
            ["-j"],
            id="enum",
        ),
        param(
            "examples/with_decimal64/interfaces.yang",
            "examples/with_decimal64/expected.json",
            ["-j"],
            id="decimal64",
        ),
        param(
            "examples/with_bits/interfaces.yang",
            "examples/with_bits/expected.json",
            ["-j"],
            id="bits",
        ),
        param(
            "examples/with_leafref2/keychains.yang",
            "examples/with_leafref2/expected.json",
            ["-j"],
            id="leafref2",
        ),
        param(
            "examples/with_identity_default_list/ciphers.yang",
            "examples/with_identity_default_list/expected.json",
            ["-j"],
            id="identity default list",
        ),
    ],
)
def test_json_schema(
    input_dir: str, expected_file: str, args: List[str], tmp_path: Path
):
    input_folder = Path(__package__) / input_dir
    expected = Path(__package__) / expected_file
    run_pydantify(
        input_file=input_folder,
        output_folder=tmp_path,
        args=args,
    )
    print("Temp file: " + str(tmp_path / "out.json"))
    expected_json = json.loads(Path(expected).read_text())
    tmp_json = json.loads(Path(tmp_path / "out.json").read_text())
    assert tmp_json == expected_json
