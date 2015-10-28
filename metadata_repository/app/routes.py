import traceback

import wtforms
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for

from .forms import DataSourceForm, TestMatchForm, UrlMatcherForm
from .models import db_session, DataSource, UrlMatcher
from .util import available_matcher_types, options_form_class_for_matcher_type

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return redirect(url_for("routes.list_data_sources"))

@routes.route("/data_sources")
def list_data_sources():
    """
    List all data sources in database.
    """
    data_sources = DataSource.query.all()
    return render_template("data_sources/index.html.jinja", data_sources=data_sources)

@routes.route("/data_sources/new", methods=["GET", "POST"])
def create_data_source():
    """
    For GET requests, show form for creating a new data source.
    For POST requests, process form and insert new data source into database.
    """
    form = DataSourceForm(request.form)
    if request.method == "POST" and form.validate():
        source = DataSource()
        form.populate_obj(source)

        try:
            db_session.add(source)
            db_session.commit()
            flash("Data source saved", "success")
            return redirect(url_for("routes.list_data_sources"))
        except:
            db_session.rollback()
            flash("Failed to save data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/new.html.jinja", form=form)

@routes.route("/data_sources/<source_id>")
def show_data_source(source_id):
    """
    Show information about a specific data source.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    return render_template("data_sources/show.html.jinja", data_source=data_source)

@routes.route("/data_sources/<source_id>/test_match", methods=["GET", "POST"])
def test_data_source_url_match(source_id):
    """
    Test whether or not a URL matches a data source.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    form = TestMatchForm(request.form)

    if request.method == "POST" and form.validate():
        if data_source.matches_url(form.test_url.data):
            flash("URL matches", "success")
        else:
            flash("URL does not match", "danger")

    return render_template("data_sources/test_url.html.jinja", data_source=data_source, form=form)

@routes.route("/data_sources/<source_id>/edit", methods=["GET", "POST"])
def edit_data_source(source_id):
    """
    For GET requests, show form for editing a data source.
    For POST requests, process form and update data source in database.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    form = DataSourceForm(request.form, data_source)

    if request.method == "POST" and form.validate():
        form.populate_obj(data_source)

        try:
            db_session.commit()
            flash("Data source updated", "success")
            return redirect(url_for("routes.show_data_source", source_id=source_id))
        except:
            db_session.rollback()
            flash("Failed to update data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/edit.html.jinja", data_source=data_source, form=form)

@routes.route("/data_sources/<source_id>/delete", methods=["GET", "POST"])
def delete_data_source(source_id):
    data_source = DataSource.query.filter(DataSource.id == source_id).first()

    if request.method == "POST":
        try:
            db_session.delete(data_source)
            db_session.commit()
            flash("Data source deleted", "success")
            return redirect(url_for("routes.list_data_sources"))
        except:
            db_session.rollback()
            flash("Failed to delete data source", "danger")
            traceback.print_exc()

    return render_template("data_sources/delete.html.jinja", data_source=data_source)

@routes.route("/data_sources/<source_id>/matchers/new", methods=["GET", "POST"])
def add_url_matcher(source_id):
    """
    Add a new URL matcher to a data source
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    form = UrlMatcherForm()

    if request.method == "GET":
        options_form_class = options_form_class_for_matcher_type(form.matcher_type.choices[0][0])
        if options_form_class:
            wtforms.form.BaseForm.__setitem__(form, "matcher_options", wtforms.fields.FormField(options_form_class))
        form.process(request.form)

    elif request.method == "POST":
        form.process(request.form)

        # Dynamically add subform for matcher options. Fields cannot be added to a
        # Form after its process method is called, so a second form must be created.
        # https://wtforms.readthedocs.org/en/latest/forms.html#wtforms.form.BaseForm.__setitem__
        form2 = UrlMatcherForm()
        if form.matcher_type.data:
            options_form_class = options_form_class_for_matcher_type(form.matcher_type.data)
            if options_form_class:
                wtforms.form.BaseForm.__setitem__(form2, "matcher_options", wtforms.fields.FormField(options_form_class))

        # Load request data into new form.
        form = form2
        form.process(request.form)

        if form.validate():
            url_matcher = UrlMatcher(
                data_source_id=data_source.id,
                matcher_type=form.matcher_type.data
            )
            if "matcher_options" in form._fields.keys() and form._fields["matcher_options"]:
                url_matcher.matcher_options = form._fields["matcher_options"].data
            else:
                url_matcher.matcher_options = {}

            try:
                db_session.add(url_matcher)
                db_session.commit()
                flash("Matcher saved", "success")
                return redirect(url_for("routes.show_data_source", source_id=data_source.id))
            except:
                db_session.rollback()
                flash("Failed to save matcher", "danger")
                traceback.print_exc()

    return render_template("url_matchers/new.html.jinja", data_source=data_source, form=form)

@routes.route("/data_sources/<source_id>/matchers/<matcher_id>")
def show_url_matcher(source_id, matcher_id):
    """
    Show information about a specific matcher.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    url_matcher = UrlMatcher.query.filter((DataSource.id == source_id) & (UrlMatcher.id == matcher_id)).first()

    return render_template("url_matchers/show.html.jinja", data_source=data_source, url_matcher=url_matcher)

@routes.route("/data_sources/<source_id>/matchers/<matcher_id>/edit", methods=["GET", "POST"])
def edit_url_matcher(source_id, matcher_id):
    """
    Edit a matcher
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    url_matcher = UrlMatcher.query.filter((DataSource.id == source_id) & (UrlMatcher.id == matcher_id)).first()
    form = UrlMatcherForm()

    if request.method == "GET":
        options_form_class = options_form_class_for_matcher_type(url_matcher.matcher_type)
        if options_form_class:
            wtforms.form.BaseForm.__setitem__(form, "matcher_options", wtforms.fields.FormField(options_form_class))
        form.process(request.form, url_matcher)

    elif request.method == "POST":
        form.process(request.form, url_matcher)

        # Dynamically add subform for matcher options. Fields cannot be added to a
        # Form after its process method is called, so a second form must be created.
        # https://wtforms.readthedocs.org/en/latest/forms.html#wtforms.form.BaseForm.__setitem__
        form2 = UrlMatcherForm()
        if form.matcher_type.data:
            options_form_class = options_form_class_for_matcher_type(form.matcher_type.data)
            if options_form_class:
                wtforms.form.BaseForm.__setitem__(form2, "matcher_options", wtforms.fields.FormField(options_form_class))

        # Load request data into new form.
        form = form2
        form.process(request.form, url_matcher)

        if form.validate():
            url_matcher.matcher_type = form.matcher_type.data
            if "matcher_options" in form._fields.keys() and form._fields["matcher_options"]:
                url_matcher.matcher_options = form._fields["matcher_options"].data
            else:
                url_matcher.matcher_options = {}

            try:
                db_session.commit()
                flash("Matcher updated", "success")
                return redirect(url_for("routes.show_url_matcher", source_id=data_source.id, matcher_id=url_matcher.id))
            except:
                db_session.rollback()
                flash("Failed to update matcher", "danger")
                traceback.print_exc()

    return render_template("url_matchers/edit.html.jinja", data_source=data_source, url_matcher=url_matcher, form=form)

@routes.route("/data_sources/<source_id>/matchers/<matcher_id>/delete", methods=["GET", "POST"])
def delete_url_matcher(source_id, matcher_id):
    """
    Delete a URL matcher. Prompt for confirmation first.
    """
    data_source = DataSource.query.filter(DataSource.id == source_id).first()
    url_matcher = UrlMatcher.query.filter((DataSource.id == source_id) & (UrlMatcher.id == matcher_id)).first()

    if request.method == "POST":
        try:
            db_session.delete(url_matcher)
            db_session.commit()
            flash("Matcher deleted", "success")
            return redirect(url_for("routes.show_data_source", source_id=data_source.id))
        except:
            db_session.rollback()
            flash("Failed to delete matcher", "danger")
            traceback.print_exc()

    return render_template("url_matchers/delete.html.jinja", data_source=data_source, url_matcher=url_matcher)

@routes.route("/data_sources/matcher_options_form")
def show_matcher_options_form():
    """
    Show options form for a specific matcher type.
    """
    matcher_type = request.args.get("matcher_type")
    if matcher_type not in available_matcher_types():
        abort(404)

    options_form_class = options_form_class_for_matcher_type(matcher_type)
    if options_form_class:
        class ContainerForm(wtforms.Form):
            """Placeholder form to render FormField with matcher type's options form class"""
            matcher_options = wtforms.fields.FormField(options_form_class)

        return render_template("url_matchers/matcher_options_form.html.jinja", form=ContainerForm())
    else:
        return ""
