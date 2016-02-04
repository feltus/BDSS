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

    also_process = []
    if editing_obj:
        also_process = [editing_obj]

    if request.method == "GET":
        initial_type_field_value = getattr(form, type_field_name).choices[0][0]
        if editing_obj:
            initial_type_field_value = getattr(editing_obj, type_field_name)
        options_form_class = subform_class_getter(initial_type_field_value)
        if options_form_class:
            wtforms.form.BaseForm.__setitem__(form, options_field_name, wtforms.fields.FormField(options_form_class))
        form.process(request.form, *also_process)

    elif request.method == "POST":
        form.process(request.form, *also_process)

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
        form.process(request.form, *also_process)

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
