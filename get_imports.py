# -*- coding: utf-8 -*-
# get_imports.py

# --- These imports are only for testing ---
# from json.decoder import *  # noqa (2 objects)
# from json.encoder import *  # noqa (some will be shown as from _json but are internal, hence the wrong statements in the results)
# from json.decoder import JSONDecoder, JSONDecodeError
# from json.encoder import JSONEncoder  # noqa
# from operator import *  # noqa


def get_imports(wildcard_min: int = 3) -> list:
    """
    Get all import statements in the immediate caller's frame.
    If imported more than `wildcard_min` objects in a module, show as `from ... import *`.
    Increase the value if needed.

    In a LeetCode editor, copy & paste this function then print.

    In console (same directory):
    >>> from get_imports import get_imports
    >>> print('\\n'.join(get_imports()))
    """
    init_dir=set(dir())

    import inspect

    # Objects from the modules below with internal names are the same as from the ones with public names.
    # Only a few common ones are listed here.
    module_name_internal_to_public = {
        '_bisect': 'bisect',
        '_heapq': 'heapq',
        '_operator': 'operator',
        '_functools': 'functools',
    }

    # Get all names in the immediate caller's frame
    frame=inspect.currentframe().f_back
    globals_dict = frame.f_globals | frame.f_locals

    # Remove default loaded modules and the current module `__name__`
    for module in ['__builtins__', __name__]:
        globals_dict.pop(module, None)
    # Remove locally imported modules if not in the caller's namespace
    for module in ['inspect',]:
        if module not in init_dir:
            globals_dict.pop(module, None)

    imports = {}
    regular_import_statements = []
    specific_import_statements = []

    # Check each object
    for name, obj in globals_dict.items():
        if name.startswith('__'):
            continue

        module = inspect.getmodule(obj)  # `getmodule` returns the module the obj is defined in, or None if not found
        if module:
            try:
                obj_name = obj.__name__
                module_name = module.__name__
                # print(name, obj_name, module_name)

                # Map names
                if module_name in module_name_internal_to_public:
                    module_name = module_name_internal_to_public[module_name]

                # Skip the current module
                if module_name == __name__:
                    continue

                # Identify the item
                if inspect.ismodule(obj) and obj_name == module_name:  # is the module itself
                    if name == obj_name:
                        regular_import_statements.append(f"import {obj_name}")
                    else:  # is an alias
                        regular_import_statements.append(f"import {obj_name} as {name}")
                else:  # is from this module
                    if module_name not in imports:
                        imports[module_name] = []
                    if name == obj_name:
                        imports[module_name].append(name)
                    else:  # is an alias
                        specific_import_statements.append(f"from {module_name} import {obj_name} as {name}")

            except AttributeError:
                pass

    # Format the specific imports
    for module, names in imports.items():
        if len(names) > wildcard_min:  # wildcard imports
            specific_import_statements.append(f"from {module} import *")
        else:
            specific_import_statements.append(f"from {module} import {', '.join(names)}")

    # Sort and return all imports as one list
    return (
        sorted(regular_import_statements, key=str.casefold) +
        sorted(specific_import_statements, key=str.casefold)
    )


def example():
    """Example imports."""
    try:
        from math import sqrt, log2, sinh  # noqa
        from operator import add  # noqa
        import numpy as np  # noqa
        # from numpy import random as rand  # noqa (same as `import numpy.random as rand`)
        import numpy.random as rand  # noqa
        import matplotlib  # noqa
        from matplotlib import cm  # noqa
        import matplotlib.pyplot as plt  # noqa
        from scipy import stats  # noqa
    except ModuleNotFoundError:
        pass
    print('\n'.join(get_imports()))


def main():
    """Prints all imports."""
    try:
        import pandas as pd  # noqa (will not be in the output)
    except ModuleNotFoundError:
        pass
    example()


###############################################################################|
if __name__ == '__main__':
    main()
