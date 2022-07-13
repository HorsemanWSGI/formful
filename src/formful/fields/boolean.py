from formful.fields.meta import Field
from formful import widgets


class BooleanField(Field):
    """
    Represents an ``<input type="checkbox">``. Set the ``checked``-status by using the
    ``default``-option. Any value for ``default``, e.g. ``default="checked"`` puts
    ``checked`` into the html-element and sets the ``data`` to ``True``
    :param false_values:
        If provided, a sequence of strings each of which is an exact match
        string of what is considered a "false" value. Defaults to the tuple
        ``(False, "false", "")``
    """

    widget = widgets.CheckboxInput()
    false_values = (False, "false", "")

    def __init__(self, label=None, validators=None, false_values=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        if false_values is not None:
            self.false_values = false_values

    def process_data(self, value):
        self.data = bool(value)

    def process_formdata(self, valuelist):
        if not valuelist or valuelist[0] in self.false_values:
            self.data = False
        else:
            self.data = True

    def _value(self):
        if self.raw_data:
            return str(self.raw_data[0])
        return "y"


class SubmitField(BooleanField):
    """
    Represents an ``<input type="submit">``.
    This allows checking if a given submit button has been pressed.
    """

    widget = widgets.SubmitInput()
