from io import TextIOWrapper
from pyang.statements import ModSubmodStatement, Statement
from pyang import statements
from pyang.context import Context
from typing import Dict, List
from ..models.models import PyangModule
from datamodel_code_generator import generate, InputFileType
from pathlib import Path


class ModelGenerator:
    @staticmethod
    def generate(ctx: Context, modules: ModSubmodStatement, fd: TextIOWrapper):
        ModelGenerator.__generate(modules, fd)

    @staticmethod
    def __generate(modules: List[Statement], fd: TextIOWrapper):
        """Generates and yealds"""
        for module in modules:
            module: ModSubmodStatement
            json = PyangModule(module).to_pydantic_schema()
            generate(json, snake_case_field=True, input_file_type=InputFileType.JsonSchema, output=Path('./out2.py'))
            pass

    @staticmethod
    def print_container(node: statements.Statement):
        class_string = ""

        class_members = ModelGenerator.syntax(node, is_attr=False)

        if node.i_children:
            for child in node.i_children:
                if child.keyword in ['leaf']:
                    class_members += ModelGenerator.syntax(child, keyword=child.keyword)
                elif child.keyword in ['leaf-list']:
                    class_members += ModelGenerator.syntax(child, keyword=child.keyword)
                elif child.keyword in ['container', 'list']:
                    # we determine if a child is a choice statement so we create the appropriate Union attr
                    if child.search_one("choice"):
                        for ch in child.i_children:
                            # we use the parent to determine the attr name or we end up with the choice name which shouldn't show up in the schema
                            class_members += ModelGenerator.syntax(ch, keyword=ch.keyword, parent=child)
                            # Choices are nested two more levels, hence the double for loop
                            for c in ch.i_children:
                                for _c in c.i_children:
                                    class_string += ModelGenerator.print_container(_c)
                    else:
                        class_members += ModelGenerator.syntax(child, keyword=child.keyword)
                        class_string += ModelGenerator.print_container(child)
        # We get here if there's a Class statement without any attributes so we add a pass
        else:
            class_members += "    pass\n"
        class_string += f"{class_members}\n\n"
        return class_string

    @staticmethod
    def syntax(node: Statement, keyword: str = None, is_attr: bool = True, parent=None) -> str:
        rv = ""
        arg = node.arg.replace("-", "_")
        if parent:
            par = parent.arg.replace("-", "_")

        if not is_attr:
            rv += f"class {arg.title()}(BaseModel):\n"
            return rv

        match keyword:
            case "leaf":
                rv += f"    {arg}: UnknownType\n"
            case "leaf-list":
                rv += f"    {arg}: List[UnknownType]\n"
            case "list":
                rv += f"    {arg}: List[{arg.title()}]\n"
            case "container":
                rv += f"    {arg}: {arg.title()}\n"
            case "choice":
                rv += f"    {par}: Union["
                chs = ",".join([child.arg.title() for child in node.i_children])
                rv += f"{chs}"
                rv += "]\n"
        return rv
