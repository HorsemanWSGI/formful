from formful.widgets.meta import Input


class CheckboxInput(Input):
    """
    Render a checkbox.
    The ``checked`` HTML attribute is set if the field's data is a non-false value.
    """

    input_type = "checkbox"

    def __call__(self, field, **kwargs):
        if getattr(field, "checked", field.data):
            kwargs["checked"] = True
        return super().__call__(field, **kwargs)


class SubmitInput(Input):
    """
    Renders a submit button.
    The field's label is used as the text of the submit button instead of the
    data on the field.
    """

    input_type = "submit"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("value", field.label.text)
        return super().__call__(field, **kwargs)
