import importlib
import json
import os
import pkgutil

import sqlalchemy
import sqlalchemy.ext.mutable


######################################################################################################
#
# Base methods
#
######################################################################################################


def _modules_in_package(package_name):
    """List of names of modules in a package."""
    modules_directory = os.path.join(os.path.dirname(__file__), package_name)
    return [name for _, name, _ in pkgutil.iter_modules([modules_directory])]


def _property_of_module(module, property_name):
    """Return a property of a module or None if the property doesn't exist."""
    try:
        module = importlib.import_module(__package__ + "." + module)
        return getattr(module, property_name)
    except (AttributeError, ImportError):
        return None


######################################################################################################
#
# URL Matchers
#
######################################################################################################


def available_matcher_types():
    """List names of available matcher modules."""
    return _modules_in_package("matchers")


def label_for_matcher_type(matcher_type):
    """Get user facing label for a matcher type."""
    label = _property_of_module("matchers." + matcher_type, "label")
    return label if label else matcher_type


def matcher_of_type(matcher_type):
    """Get matcher function for a matcher type."""
    return _property_of_module("matchers." + matcher_type, "matches_url")


def options_form_class_for_matcher_type(matcher_type):
    """Get options form for a matcher type."""
    return _property_of_module("matchers." + matcher_type, "OptionsForm")


######################################################################################################
#
# URL Transforms
#
######################################################################################################


def available_transform_types():
    """List names of available matcher modules."""
    return _modules_in_package("transforms")


def label_for_transform_type(transform_type):
    """Get user facing label for a transform type."""
    label = _property_of_module("transforms." + transform_type, "label")
    return label if label else transform_type


def transform_of_type(transform_type):
    """Get matcher function for a transform type."""
    return _property_of_module("transforms." + transform_type, "transform_url")


def options_form_class_for_transform_type(transform_type):
    """Get options form for a transform type."""
    return _property_of_module("transforms." + transform_type, "OptionsForm")


######################################################################################################
#
# Transfer mechanisms
#
######################################################################################################


def available_transfer_mechanism_types():
    """List names of available transfer mechanism modules."""
    return _modules_in_package("transfer_mechanisms")


def label_for_transfer_mechanism_type(transfer_mechanism_type):
    """Get user facing label for a transfer mechanism type."""
    label = _property_of_module("transfer_mechanisms." + transfer_mechanism_type, "label")
    return label if label else transfer_mechanism_type


def options_form_class_for_transfer_mechanism_type(transfer_mechanism_type):
    """Get options form for a transfer_mechanism type."""
    return _property_of_module("transfer_mechanisms." + transfer_mechanism_type, "OptionsForm")


######################################################################################################
#
# Database types
#
######################################################################################################


class JSONEncodedDict(sqlalchemy.types.TypeDecorator):
    """
    This type stores data in the database as JSON encoded text.
    However, the model's property is a dictionary.

    http://docs.sqlalchemy.org/en/latest/core/custom_types.html#marshal-json-strings
    """

    impl = sqlalchemy.types.Text

    def process_bind_param(self, value, dialect):
        """Store dictionary as JSON."""
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """Load dictionary from JSON."""
        if value is not None:
            value = json.loads(value)
        return value


class MutableDict(sqlalchemy.ext.mutable.Mutable, dict):
    """
    Used in conjunctino with JSONEncodedDict.
    By default, when a dictionary value is changed, the dictionary object is still the same object, so SQLAlchemy
    doesn't recognize the field as having changed and thus doesn't store the change in the database.

    This marks the field as having changed whenever a dictionary value is changed or a key is deleted.

    http://docs.sqlalchemy.org/en/latest/orm/extensions/mutable.html#establishing-mutability-on-scalar-column-values
    """

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."
        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)
            return sqlalchemy.ext.mutable.Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."
        dict.__delitem__(self, key)
        self.changed()
