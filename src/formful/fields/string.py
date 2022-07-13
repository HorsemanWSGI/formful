from formful.fields.meta import Field
from formful import widgets


class StringField(Field):
    """
    This field is the base for most of the more complicated fields, and
    represents an ``<input type="text">``.
    """

    widget = widgets.TextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]

    def _value(self):
        return str(self.data) if self.data is not None else ""


class TextAreaField(StringField):
    """
    This field represents an HTML ``<textarea>`` and can be used to take
    multi-line input.
    """

    widget = widgets.TextArea()


class PasswordField(StringField):
    """
    A StringField, except renders an ``<input type="password">``.
    Also, whatever value is accepted by this field is not rendered back
    to the browser like normal fields.
    """

    widget = widgets.PasswordInput()


class SearchField(StringField):
    """
    Represents an ``<input type="search">``.
    """

    widget = widgets.SearchInput()


class TelField(StringField):
    """
    Represents an ``<input type="tel">``.
    """

    widget = widgets.TelInput()


class URLField(StringField):
    """
    Represents an ``<input type="url">``.
    """

    widget = widgets.URLInput()


class EmailField(StringField):
    """
    Represents an ``<input type="email">``.
    """

    widget = widgets.EmailInput()


class HiddenField(StringField):
    """
    HiddenField is a convenience for a StringField with a HiddenInput widget.
    It will render as an ``<input type="hidden">`` but otherwise coerce to a string.
    """

    widget = widgets.HiddenInput()
