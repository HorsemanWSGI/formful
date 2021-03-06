import pytest

from formful import validators
from formful.fields import StringField
from formful.form import Form


@pytest.fixture()
def flags():
    return StringField(
        validators=[validators.DataRequired()]
    ).bind(Form(), "a").flags


def test_existing_values(flags):
    assert flags.required is True
    assert "required" in flags
    assert flags.optional is None
    assert "optional" not in flags


def test_assignment(flags):
    assert "optional" not in flags
    flags.optional = True
    assert flags.optional is True
    assert "optional" in flags


def test_unset(flags):
    flags.required = False
    assert flags.required is False
    assert "required" not in flags


def test_repr(flags):
    assert repr(flags) == "<formful.fields.Flags: {required}>"


def test_underscore_property(flags):
    with pytest.raises(AttributeError):
        flags._foo
    flags._foo = 42
    assert flags._foo == 42
