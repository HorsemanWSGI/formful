from datetime import datetime
from tests.common import DummyPostData
from formful.fields import TimeField
from formful.form import Form


def make_form(**fields):
    return Form(fields)


def test_basic():
    d = datetime(2008, 5, 5, 4, 30, 0, 0).time()
    form = make_form(a=TimeField(), b=TimeField(format="%H:%M"))

    # Basic test with both inputs
    form.process(DummyPostData(a=["4:30"], b=["04:30"]))
    assert form.fields['a'].data == d
    assert form.fields['a']() == (
        """<input id="a" name="a" type="time" value="4:30">""")

    assert form.fields['b'].data == d
    assert form.fields['b']() == (
        """<input id="b" name="b" type="time" value="04:30">"""
    )
    assert form.validate()

    # Test with a missing input
    form.process(DummyPostData(a=["04"]))
    assert not form.validate()
    assert form.fields['a'].errors[0] == "Not a valid time value."
