import logging
import os
import time
from io import TextIOWrapper
from typing import Dict

import psutil
from pyang.context import Context
from pyang.plugin import PyangPlugin, register_plugin
from pyang.statements import ModSubmodStatement

from pydantify.utility.model_generator import ModelGenerator

logger = logging.getLogger("pydantify")


def pyang_plugin_init():
    register_plugin(Pydantify())
    logger.debug("Plugin successfully registered.")


class Pydantify(PyangPlugin):
    def __init__(self):
        """Init plugin instance."""
        super().__init__(name="pydantify")

    def add_output_format(self, fmts: Dict[str, PyangPlugin]):
        """Register self as primary pydantic output generator."""
        fmts["pydantic"] = self
        self.multiple_modules = True
        self.handle_comments = True
        logger.debug("Plugin registered for pydantic format.")

    def emit(self, ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        """Convert yang model."""
        start = psutil.Process(os.getpid()).create_time()
        logger.debug(f"Pyang completed parsing in {time.time() - start:.3f}s.")

        start = time.time()
        ModelGenerator.generate(ctx=ctx, modules=modules, fd=fd)
        logger.info(f"Output model generated in {time.time() - start:.3f}s.")
