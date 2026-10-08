# -*- coding: utf-8 -*-
"""Import a chapter file by path.

Every chapter has a content.py, a pages.py, an audio_script.py … with the same
names, so they cannot be imported the normal way: the second chapter would get
the first one's module back from the cache. Each is loaded from its own path.
"""
import importlib.util
import sys


def load(path, name, register=False):
    """Import the file at `path` as a module called `name`.

    register=True also puts it in sys.modules, for a file that another one
    imports by name — pages.py does `from content import *`.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    if register:
        sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod
