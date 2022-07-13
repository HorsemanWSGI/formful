from formful.fields.meta import Field
from formful import widgets


class FileField(Field):
    """Renders a file upload field.
    By default, the value will be the filename sent in the form data.
    WTForms **does not** deal with frameworks' file handling capabilities.
    A WTForms extension for a framework may replace the filename value
    with an object representing the uploaded data.
    """

    widget = widgets.FileInput()

    def _value(self):
        # browser ignores value of file input for security
        return False


class MultipleFileField(FileField):
    """A :class:`FileField` that allows choosing multiple files."""

    widget = widgets.FileInput(multiple=True)

    def process_formdata(self, valuelist):
        self.data = valuelist
