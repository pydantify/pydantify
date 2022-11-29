import logging
from io import TextIOWrapper
from typing import Dict

from pyang.context import Context
from pyang.plugin import PyangPlugin, register_plugin
from pyang.statements import ModSubmodStatement

from pydantify.models import ModelGenerator

logger = logging.getLogger('pydantify')


def pyang_plugin_init():
    register_plugin(Pydantify())
    logger.debug('Plugin successfully registered.')


class Pydantify(PyangPlugin):
    def __init__(self):
        """Init plugin instance."""
        super().__init__(name="pydantify")

    def add_output_format(self, fmts: Dict[str, PyangPlugin]):
        """Register self as primary pydantic output generator."""
        fmts['pydantic'] = self
        self.multiple_modules = True
        self.handle_comments = True
        logger.debug('Plugin registered for pydantic format.')

    def emit(self, ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        """Convert yang model."""
        logger.debug('Pyang parsing complete. Beginning output creation.')
        ModelGenerator.generate(ctx=ctx, modules=modules, fd=fd)
