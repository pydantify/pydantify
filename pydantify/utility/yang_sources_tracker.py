import logging
import os
import shutil
from pathlib import Path
from typing import Set, Type

from pyang.error import Position
from typing_extensions import Self

logger = logging.getLogger("pydantify")


class YANGSourcesTracker:
    @classmethod
    def track_from_pos(cls: Type[Self], pos: Position):
        path = str(Path(pos.ref).absolute())
        cls._relevant_files.add(path)

    # TODO: Is this necessary?
    # Pytest does not reset static class variable otherwise.
    @classmethod
    @property
    def _relevant_files(cls):
        if not hasattr(cls, "__relevant_files"):
            cls.__relevant_files: Set[str] = set()
        return cls.__relevant_files

    @classmethod
    def copy_yang_files(cls: Type[Self], input_root: Path, output_dir: Path):
        """Copy only the relevant YANG model files to the output directory."""
        for f in cls._relevant_files:
            out_path = output_dir
            if input_root is not None:
                delta: Path = Path(f).parent.relative_to(input_root)
                out_path: Path = output_dir.joinpath(delta)
                if not out_path.exists():
                    os.makedirs(out_path, exist_ok=True)
            out = shutil.copy2(f, out_path)
            logger.debug(f'Copied file "{f}" -> "{out}"')
