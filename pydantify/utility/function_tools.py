import inspect
from typing import Callable
import re


def function_to_source_code(f: Callable) -> str:
    return inspect.getsource(f)


def function_content_to_source_code(f: Callable) -> str:
    src = inspect.getsourcelines(f)[0]
    indentation = re.compile('^([\t ]+)').findall(src[1])[0]
    return "".join(line.replace(indentation, '', 1) for line in src[1:])
