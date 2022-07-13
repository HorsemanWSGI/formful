import datetime
from formful.fields.meta import Field
from formful import widgets


class DateTimeField(Field):
    """
    A text field which stores a `datetime.datetime` matching a format.
    """

    widget = widgets.DateTimeInput()

    def __init__(
        self, label=None, validators=None, format="%Y-%m-%d %H:%M:%S", **kwargs
    ):
        super().__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return " ".join(self.raw_data)
        return self.data and self.data.strftime(self.format) or ""

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        date_str = " ".join(valuelist)
        try:
            self.data = datetime.datetime.strptime(date_str, self.format)
        except ValueError:
            self.data = None
            raise ValueError(self.gettext("Not a valid datetime value."))


class DateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """

    widget = widgets.DateInput()

    def __init__(self, label=None, validators=None, format="%Y-%m-%d", **kwargs):
        super().__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        date_str = " ".join(valuelist)
        try:
            self.data = datetime.datetime.strptime(date_str, self.format).date()
        except ValueError:
            self.data = None
            raise ValueError(self.gettext("Not a valid date value."))


class TimeField(DateTimeField):
    """
    Same as DateTimeField, except stores a `time`.
    """

    widget = widgets.TimeInput()

    def __init__(self, label=None, validators=None, format="%H:%M", **kwargs):
        super().__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        time_str = " ".join(valuelist)
        try:
            self.data = datetime.datetime.strptime(time_str, self.format).time()
        except ValueError:
            self.data = None
            raise ValueError(self.gettext("Not a valid time value."))


class MonthField(DateField):
    """
    Same as DateField, except represents a month, stores a `datetime.date`
    with `day = 1`.
    """

    widget = widgets.MonthInput()

    def __init__(self, label=None, validators=None, format="%Y-%m", **kwargs):
        super().__init__(label, validators, format, **kwargs)


class DateTimeLocalField(DateTimeField):
    """
    Represents an ``<input type="datetime-local">``.
    """

    widget = widgets.DateTimeLocalInput()
