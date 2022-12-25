import inspect
from typing import Callable
import re


def function_to_source_code(f: Callable) -> str:
    return inspect.getsource(f)


def function_content_to_source_code(f: Callable) -> str:
    function_lines: list[str] = inspect.getsourcelines(f)[0]
    function_content = function_lines[1:]
    indentation = re.compile("^([\t ]+)").findall(function_content[0])[0]
    return "".join(line.replace(indentation, "", 1) for line in function_content)
