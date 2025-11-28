import importlib.util
import json
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, List
from unittest.mock import patch

import pytest
from pytest import param

LOGGER = logging.getLogger(__name__)


def import_from_path(module_name: str, file_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module {module_name} at {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    if spec.loader is None:
        raise ImportError(f"Could not load module {module_name} from {file_path}")
    spec.loader.exec_module(module)
    return module


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
    ("input_dir", "sample_file", "args", "dump_options"),
    [
        param(
            "examples/minimal/interfaces.yang",
            "examples/minimal/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="minimal",
        ),
        param(
            "examples/with_typedef/interfaces.yang",
            "examples/with_typedef/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="typedef",
        ),
        param(
            "examples/with_leafref/interfaces.yang",
            "examples/with_leafref/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="leafref",
        ),
        param(
            "examples/with_restrictions/interfaces.yang",
            "examples/with_restrictions/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="restrictions",
        ),
        param(
            "examples/with_uses/interfaces.yang",
            "examples/with_uses/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="uses",
        ),
        param(
            "examples/with_case/interfaces.yang",
            "examples/with_case/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="case",
        ),
        param(
            "examples/with_complex_case/interfaces.yang",
            "examples/with_complex_case/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="complex case",
        ),
        param(
            "examples/turing-machine/turing-machine.yang",
            "examples/turing-machine/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="turing machine",
        ),
        param(
            "examples/with_leaflist/interfaces.yang",
            "examples/with_leaflist/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="leaf-list",
        ),
        param(
            "examples/with_union/interfaces.yang",
            "examples/with_union/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="type union",
        ),
        param(
            "examples/with_identity_default/interfaces.yang",
            "examples/with_identity_default/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="identity default",
        ),
        param(
            "examples/with_enum/interfaces.yang",
            "examples/with_enum/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="enum",
        ),
        param(
            "examples/with_decimal64/interfaces.yang",
            "examples/with_decimal64/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="decimal64",
        ),
        param(
            "examples/with_bits/interfaces.yang",
            "examples/with_bits/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="bits",
        ),
        param(
            "examples/with_leafref2/keychains.yang",
            "examples/with_leafref2/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="leafref2",
        ),
        param(
            "examples/with_identity_default_list/ciphers.yang",
            "examples/with_identity_default_list/sample_data.json",
            [],
            {"exclude_defaults": False, "mode": "json"},
            id="identity default list",
        ),
        param(
            "examples/with_empty/interface.yang",
            "examples/with_empty/sample_data.json",
            [],
            {"exclude_defaults": True, "mode": "json"},
            id="empty",
        ),
    ],
)
def test_model(
    input_dir: str,
    sample_file: str,
    args: List[str],
    dump_options: dict[str, Any],
    tmp_path: Path,
):
    input_folder = Path(__package__) / input_dir
    sample_data = json.loads((Path(__package__) / sample_file).read_text())
    run_pydantify(
        input_file=input_folder,
        output_folder=tmp_path,
        args=args,
    )
    module = import_from_path("out", tmp_path / "out.py")
    model = module.Model.model_validate(sample_data)
    dumped_data = model.model_dump(
        **dump_options,
    )
    assert dumped_data == sample_data
