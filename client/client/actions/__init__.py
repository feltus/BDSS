import importlib
import pkgutil
import re


def all_actions():
    return [re.sub(r"_action$", "", name) for _, name, _ in pkgutil.iter_modules(__path__)]


def action_module(action_name):
    try:
        return importlib.import_module(__package__ + "." + action_name + "_action")
    except ImportError:
        return None
