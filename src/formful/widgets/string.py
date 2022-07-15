from markupsafe import Markup, escape
from formful.utils import html_params
from formful.widgets.meta import Input


class TextInput(Input):
    """
    Render a single-line text input.
    """

    input_type = "text"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]


class PasswordInput(Input):
    """
    Render a password input.
    For security purposes, this field will not reproduce the value on a form
    submit by default. To have the value filled in, set `hide_value` to
    `False`.
    """

    input_type = "password"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]

    def __init__(self, hide_value=True):
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs["value"] = ""
        return super().__call__(field, **kwargs)


class HiddenInput(Input):
    """
    Render a hidden input.
    """

    input_type = "hidden"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_flags = {"hidden": True}


class TextArea:
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    validation_attrs = ["required", "maxlength", "minlength"]

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        return Markup(
            "<textarea %s>\r\n%s</textarea>"
            % (html_params(name=field.name, **kwargs), escape(field._value()))
        )


class SearchInput(Input):
    """
    Renders an input with type "search".
    """

    input_type = "search"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]


class TelInput(Input):
    """
    Renders an input with type "tel".
    """

    input_type = "tel"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]


class URLInput(Input):
    """
    Renders an input with type "url".
    """

    input_type = "url"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]


class EmailInput(Input):
    """
    Renders an input with type "email".
    """

    input_type = "email"
    validation_attrs = ["required", "maxlength", "minlength", "pattern"]
