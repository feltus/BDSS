# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import importlib
import os
import pkgutil


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


def description_for_matcher_type(matcher_type):
    return _property_of_module("matchers." + matcher_type, "description") or ""


def matcher_of_type(matcher_type):
    """Get matcher function for a matcher type."""
    return _property_of_module("matchers." + matcher_type, "matches_url")


def options_form_class_for_matcher_type(matcher_type):
    """Get options form for a matcher type."""
    return _property_of_module("matchers." + matcher_type, "OptionsForm")


def render_matcher_description(matcher_type, matcher_options):
    """Text to show in list of matchers on show data source page."""
    return _property_of_module("matchers." + matcher_type, "render_description")(matcher_options)


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


def description_for_transform_type(transform_type):
    return _property_of_module("transforms." + transform_type, "description") or ""


def transform_of_type(transform_type):
    """Get matcher function for a transform type."""
    return _property_of_module("transforms." + transform_type, "transform_url")


def options_form_class_for_transform_type(transform_type):
    """Get options form for a transform type."""
    return _property_of_module("transforms." + transform_type, "OptionsForm")


def render_transform_description(transform_type, transform_options):
    """Text to show in list of transforms on show data source page."""
    return _property_of_module("transforms." + transform_type, "render_description")(transform_options)


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


def description_for_transfer_mechanism_type(transfer_mechanism_type):
    return _property_of_module("transfer_mechanisms." + transfer_mechanism_type, "description") or ""


def options_form_class_for_transfer_mechanism_type(transfer_mechanism_type):
    """Get options form for a transfer_mechanism type."""
    return _property_of_module("transfer_mechanisms." + transfer_mechanism_type, "OptionsForm")
