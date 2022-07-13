from formful.fields.meta import Field
from formful import widgets


class IntegerField(Field):
    """
    A text field, except all input is coerced to an integer.  Erroneous input
    is ignored and will not be accepted as a value.
    """

    widget = widgets.NumberInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data is not None:
            return str(self.data)
        return ""

    def process_data(self, value):
        if value is None or value is unset_value:
            self.data = None
            return

        try:
            self.data = int(value)
        except (ValueError, TypeError):
            self.data = None
            raise ValueError(self.gettext("Not a valid integer value."))

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = int(valuelist[0])
        except ValueError:
            self.data = None
            raise ValueError(self.gettext("Not a valid integer value."))


class FloatField(Field):
    """
    A text field, except all input is coerced to an float.  Erroneous input
    is ignored and will not be accepted as a value.
    """

    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data is not None:
            return str(self.data)
        return ""

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        try:
            self.data = float(valuelist[0])
        except ValueError:
            self.data = None
            raise ValueError(self.gettext("Not a valid float value."))


class IntegerRangeField(IntegerField):
    """
    Represents an ``<input type="range">``.
    """

    widget = widgets.RangeInput()
