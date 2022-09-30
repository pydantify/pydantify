from pyang.plugin import PyangPlugin, register_plugin
from pyang import util
from pyang import statements


def pyang_plugin_init():
    register_plugin(Yang2Pydantic())


class Yang2Pydantic(PyangPlugin):
    def __init__(self):
        """Init plugin instance."""
        super().__init__(name="yang2pydantic")

    def add_output_format(self, fmts):
        """Register self as primary pydantic output generator."""
        fmts['pydantic'] = self
        self.multiple_modules = True

    def emit(self, ctx, modules, fd):
        """Convert yang model."""
        pass
