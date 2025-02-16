# list_python_imports

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![python](https://img.shields.io/badge/Python-3.10,_3.11-3776AB?logo=python&logoColor=white)](https://www.python.org)

The function `get_imports` in the module is used to get all import statements in the immediate caller's frame.
If imported more than `wildcard_min` objects in a module, show as `from ... import *`.
Increase the value if needed.

The original intention was to check the imports in LeetCode's Python3 environment.
For example, in a LeetCode editor, copy & paste the entire function `get_imports` and call by `print('\n'.join(get_imports()))` to print the results to stdout.
