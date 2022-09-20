#!/usr/bin/env python


def start():
    print('Success!')

    from .submodule import importedFunction
    importedFunction()


if __name__ == "__main__":
    start()
