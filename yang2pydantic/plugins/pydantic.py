from io import TextIOWrapper
from pyang.plugin import PyangPlugin, register_plugin
from pyang import util
from pyang import statements
from pyang.context import Context
from typing import Dict



def pyang_plugin_init():
    register_plugin(Yang2Pydantic())


class Yang2Pydantic(PyangPlugin):
    def __init__(self):
        """Init plugin instance."""
        super().__init__(name="yang2pydantic")

    def add_output_format(self, fmts: Dict[str, PyangPlugin]):
        """Register self as primary pydantic output generator."""
        fmts['pydantic'] = self
        self.multiple_modules = True
        self.handle_comments = True

    def emit(self, ctx: Context, modules, fd: TextIOWrapper):
        """Convert yang model."""
        self.__write_imports(fd)
        self.__generate(modules, fd)

    def __generate(self, modules, fd: TextIOWrapper):
        """Generates and yealds """
        for module in modules:
            chs = [ch for ch in module.i_children
                if ch.keyword in statements.data_definition_keywords]

            if len(chs) > 0:
                for ch in chs:
                    fd.write(self.print_container(ch))

            mods = [module]
            for m in mods:
                for augment in m.search('augment'):
                    if hasattr(augment, 'i_children'):
                        chs = [ch for ch in augment.i_children if ch.keyword in statements.data_definition_keywords]

                        if len(chs) > 0:
                            for ch in chs:
                                fd.write(self.print_container(ch))

    def print_container(self, node: statements.Statement):
        paths = ""

        path = self.syntax(node, is_attr=False)

        if node.i_children:
            for child in node.i_children:
                if child.keyword in ['leaf']:
                    path += self.syntax(child, keyword=child.keyword)
                elif child.keyword in ['leaf-list']:
                    path += self.syntax(child, keyword=child.keyword)
                elif child.keyword in ['container', 'list']:
                    # we determine if a child is a choice statement so we create the appropriate Union attr
                    if child.search_one("choice"):
                        for ch in child.i_children:
                            # we use the parent to determine the attr name or we end up with the choice name which shouldn't show up in the schema
                            path += self.syntax(ch, keyword=ch.keyword, parent=child)
                            # Choices are nested two more levels, hence the double for loop
                            for c in ch.i_children:
                                for _c in c.i_children:
                                    paths += self.print_container(_c)
                    else:
                        path += self.syntax(child, keyword=child.keyword)
                        paths += self.print_container(child)
        # We get here if there's a Class statement without any attributes so we add a pass
        else:
            path += "    pass\n"

        paths += f"{path}\n"
        return paths

    def syntax(self, node, keyword=None, is_attr=True, parent=None) -> str:
        rv = ""
        arg = node.arg.replace("-", "_")
        if parent:
            par = parent.arg.replace("-", "_")

        if is_attr == False:
            rv += f"class {arg.title()}(BaseModel):\n"
            return rv

        match keyword:
            case "leaf":
                rv += f"    {arg}: \n"
            case "leaf-list":
                rv += f"    {arg}: List[str]\n"
            case "list":
                rv += f"    {arg}: List[{arg.title()}]\n"
            case "container":
                rv += f"    {arg}: {arg.title()}\n"
            case "choice":
                rv += f"    {par}: Union["
                chs = ",".join([child.arg.title() for child in node.i_children])
                rv += f"{chs}"
                rv += f"]\n"
        return rv

    def __write_imports(self, fd: TextIOWrapper):
        fd.writelines([
            "from typing import List, Optional, Union",
            "from pydantic import BaseModel, Field"
        ])
