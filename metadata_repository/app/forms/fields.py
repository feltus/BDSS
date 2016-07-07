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


class SelectWithOptionDescription(wtforms.widgets.Select):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "class_" in kwargs:
            kwargs["class_"] += " option-descriptions"
        else:
            kwargs["class_"] = "option-descriptions"

        if self.multiple:
            kwargs["multiple"] = True
        html = ["<select %s>" % wtforms.widgets.html_params(name=field.name, **kwargs)]
        for val, label, selected, option_description in field.iter_choices_with_description():
            html.append(self.render_option(val, label, selected, data_description=option_description))
        html.append("</select>")
        return wtforms.widgets.HTMLString("".join(html))


class SelectWithOptionDescriptionField(wtforms.fields.SelectField):

    widget = SelectWithOptionDescription()

    def __init__(self, label=None, validators=None, coerce=wtforms.compat.text_type, choices=None, option_descriptions=None, **kwargs):
        super(SelectWithOptionDescriptionField, self).__init__(label, validators, coerce, choices, **kwargs)
        if option_descriptions:
            self.option_descriptions = option_descriptions
        else:
            self.option_descriptions = ["" for c in choices]

    def iter_choices_with_description(self):
        for (i, (value, label)) in enumerate(self.choices):
            yield (value, label, self.coerce(value) == self.data, self.option_descriptions[i])
