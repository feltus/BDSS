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

import wtforms
from flask import abort, render_template, request


def process_form_with_options_subform(form_class, type_field_name, options_field_name, subform_class_getter, editing_obj=None, form_init=None):
    """
    form_class - class
    type_field_name - string
    options_field_name - string
    subform_class_getter - callable
    form_init - callable
    """
    form = form_class()
    if form_init:
        form_init(form)

    if request.method == "GET":
        initial_type_field_value = getattr(form, type_field_name).choices[0][0]
        if editing_obj:
            initial_type_field_value = getattr(editing_obj, type_field_name)
        options_form_class = subform_class_getter(initial_type_field_value)
        if options_form_class:
            wtforms.form.BaseForm.__setitem__(form, options_field_name, wtforms.fields.FormField(options_form_class))
        form.process(request.form, obj=editing_obj)

    elif request.method == "POST":
        form.process(request.form, obj=editing_obj)

        # Dynamically add subform for transform options. Fields cannot be added to a
        # Form after its process method is called, so a second form must be created.
        # https://wtforms.readthedocs.org/en/latest/forms.html#wtforms.form.BaseForm.__setitem__
        form2 = form_class()
        if form_init:
            form_init(form2)
        if getattr(form, type_field_name).data:
            options_form_class = subform_class_getter(getattr(form, type_field_name).data)
            if options_form_class:
                wtforms.form.BaseForm.__setitem__(form2, options_field_name, wtforms.fields.FormField(options_form_class))

        # Load request data into new form.
        form = form2
        form.process(request.form, obj=editing_obj)

    return form


def render_options_subform(valid_types, form_class_getter, type_field_name):
    t = request.args.get("type")
    if t not in valid_types:
        abort(404)

    options_form_class = form_class_getter(t)
    if options_form_class:
        class ContainerForm(wtforms.Form):
            """Placeholder form to render FormField"""
            pass

        setattr(ContainerForm, type_field_name, wtforms.fields.FormField(options_form_class))

        return render_template("options_form.html.jinja", form=ContainerForm())
    else:
        abort(500)
