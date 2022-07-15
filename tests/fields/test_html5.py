from datetime import date
from datetime import datetime
from tests.common import DummyPostData

from formful import validators
from formful.fields import DateField
from formful.fields import DateTimeField
from formful.fields import DateTimeLocalField
from formful.fields import EmailField
from formful.fields import IntegerField
from formful.fields import IntegerRangeField
from formful.fields import PasswordField
from formful.fields import SearchField
from formful.fields import StringField
from formful.fields import TelField
from formful.fields import TextAreaField
from formful.fields import URLField
from formful.schema import Schema
from formful.utils import unset_value


class Fields(Schema):
    search = SearchField()
    telephone = TelField()
    url = URLField()
    email = EmailField()
    datetime = DateTimeField()
    date = DateField()
    dt_local = DateTimeLocalField()
    integer = IntegerField()
    int_range = IntegerRangeField()


def _build_value(key, form_input, expected_html, data=unset_value):
    if data is unset_value:
        data = form_input
    if expected_html.startswith("type="):
        expected_html = '<input id="{}" name="{}" {} value="{}">'.format(
            key, key, expected_html, form_input
        )
    return {
        "key": key,
        "form_input": form_input,
        "expected_html": expected_html,
        "data": data,
    }


def test_simple():
    b = _build_value
    VALUES = (
        b("search", "search", 'type="search"'),
        b("telephone", "123456789", 'type="tel"'),
        b("url", "http://formful.simplecodes.com/", 'type="url"'),
        b("email", "foo@bar.com", 'type="email"'),
        b(
            "datetime",
            "2013-09-05 00:23:42",
            'type="datetime"',
            datetime(2013, 9, 5, 0, 23, 42),
        ),
        b("date", "2013-09-05", 'type="date"', date(2013, 9, 5)),
        b(
            "dt_local",
            "2013-09-05 00:23:42",
            'type="datetime-local"',
            datetime(2013, 9, 5, 0, 23, 42),
        ),
        b(
            "integer",
            "42",
            '<input id="integer" name="integer" type="number" value="42">',
            42,
        ),
        b(
            "decimal",
            "43.5",
            '<input id="decimal" name="decimal" '
            'step="any" type="number" value="43.5">',
            Decimal("43.5"),
        ),
        b(
            "int_range",
            "4",
            '<input id="int_range" name="int_range" type="range" value="4">',
            4,
        ),
        b(
            "decimal_range",
            "58",
            '<input id="decimal_range" name="decimal_range" '
            'step="any" type="range" value="58">',
            58,
        ),
    )
    formdata = DummyPostData()
    kw = {}
    for item in VALUES:
        formdata[item["key"]] = item["form_input"]
        kw[item["key"]] = item["data"]

    form = F(formdata)
    for item in VALUES:
        field = form[item["key"]]
        render_value = field()
        if render_value != item["expected_html"]:
            tmpl = "Field {key} render mismatch: {render_value!r} != {expected_html!r}"
            raise AssertionError(tmpl.format(render_value=render_value, **item))
        if field.data != item["data"]:
            tmpl = "Field {key} data mismatch: {field.data!r} != {data!r}"
            raise AssertionError(tmpl.format(field=field, **item))


class FieldsWithValidators(Schema):
    v1 = [validators.Length(min=1)]
    v2 = [validators.Length(min=1, max=3)]
    string1 = StringField(validators=v1)
    string2 = StringField(validators=v2)
    password1 = PasswordField(validators=v1)
    password2 = PasswordField(validators=v2)
    textarea1 = TextAreaField(validators=v1)
    textarea2 = TextAreaField(validators=v2)
    search1 = SearchField(validators=v1)
    search2 = SearchField(validators=v2)

    v3 = [validators.NumberRange(min=1)]
    v4 = [validators.NumberRange(min=1, max=3)]
    integer1 = IntegerField(validators=v3)
    integer2 = IntegerField(validators=v4)
    integerrange1 = IntegerRangeField(validators=v3)
    integerrange2 = IntegerRangeField(validators=v4)


def test_minlength_maxlength():
    form = Form(FieldsWithValidators)
    form.process()
    assert (
        form.string1()
        == '<input id="string1" minlength="1" name="string1" type="text" value="">'
    )

    assert (
        form.string2() == '<input id="string2" maxlength="3" minlength="1"'
        ' name="string2" type="text" value="">'
    )

    assert (
        form.password1() == '<input id="password1" minlength="1"'
        ' name="password1" type="password" value="">'
    )

    assert (
        form.password2() == '<input id="password2" maxlength="3" minlength="1"'
        ' name="password2" type="password" value="">'
    )

    assert (
        form.textarea1() == '<textarea id="textarea1" minlength="1"'
        ' name="textarea1">\r\n</textarea>'
    )

    assert (
        form.textarea2() == '<textarea id="textarea2" maxlength="3" minlength="1"'
        ' name="textarea2">\r\n</textarea>'
    )

    assert (
        form.search1() == '<input id="search1" minlength="1"'
        ' name="search1" type="search" value="">'
    )

    assert (
        form.search2() == '<input id="search2" maxlength="3" minlength="1"'
        ' name="search2" type="search" value="">'
    )


def test_min_max():
    form = Form(FieldsWithValidators)
    form.process()
    assert (
        form.integer1()
        == '<input id="integer1" min="1" name="integer1" type="number" value="">'
    )
    assert (
        form.integer2() == '<input id="integer2" max="3" min="1"'
        ' name="integer2" type="number" value="">'
    )

    assert (
        form.integerrange1() == '<input id="integerrange1" min="1"'
        ' name="integerrange1" type="range" value="">'
    )

    assert (
        form.integerrange2() == '<input id="integerrange2" max="3" min="1"'
        ' name="integerrange2" type="range" value="">'
    )
