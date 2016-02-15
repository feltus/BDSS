import importlib
import pkgutil


EXCLUDE_MODULES = ("base",)


def available_mechanisms():
    """
    Names of all available transfer mechanisms.
    """
    return [name for _, name, _ in pkgutil.iter_modules(__path__) if name not in EXCLUDE_MODULES]


def default_mechanism(url):
    """
    Name of the default transfer mechanism for a URL.
    This is used if the metadata repository doesn't specify a mechanism.

    Returns
    Tuple of mechanism name and options.
    """
    return ("curl", None)


def transfer_mechanism_module(mechanism_name):
    """
    The Python module for a transfer mechanism.
    """
    try:
        return importlib.import_module(__package__ + "." + mechanism_name)
    except ImportError:
        return None
