from markupsafe import Markup, escape
from formful.utils import html_params
from formful.widgets.meta import Input


class Select:
    """
    Renders a select field.
    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.
    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """

    validation_attrs = ["required"]

    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        html = ["<select %s>" % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = str(value)

        options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        return Markup(
            "<option {}>{}</option>".format(
                html_params(**options), escape(label)
            )
        )


class Option:
    """
    Renders the individual option from a select field.
    This is just a convenience for various custom rendering situations, and an
    option by itself does not constitute an entire field.
    """

    def __call__(self, field, **kwargs):
        return Select.render_option(
            field._value(), field.label.text, field.checked, **kwargs
        )


class RadioInput(Input):
    """
    Render a single radio button.
    This widget is most commonly used in conjunction with ListWidget or some
    other listing, as singular radio buttons are not very useful.
    """

    input_type = "radio"

    def __call__(self, field, **kwargs):
        if field.checked:
            kwargs["checked"] = True
        return super().__call__(field, **kwargs)
