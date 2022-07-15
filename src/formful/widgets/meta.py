from markupsafe import Markup, escape
from formful.utils import html_params


class Input:
    """
    Render a basic ``<input>`` field.
    This is used as the basis for most of the other input fields.
    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    html_params = staticmethod(html_params)
    validation_attrs = ["required"]

    def __init__(self, input_type=None):
        if input_type is not None:
            self.input_type = input_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        return Markup(
            "<input %s>" % self.html_params(name=field.name, **kwargs)
        )
