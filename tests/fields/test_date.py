from datetime import date

from tests.common import DummyPostData

from formful.fields import DateField
from formful.form import Form
from formful.schema import Schema


F = Form(fields={
    'a': DateField(),
    'b': DateField(format="%m/%d %Y"),
    'c': DateField(format="%-m/%-d %Y"),
})


def test_basic():
    d = date(2008, 5, 7)
    F.process(DummyPostData(
        a=["2008-05-07"],
        b=["05/07", "2008"],
        c=["5/7 2008"]
    ))
    assert F['a'].data == d
    assert F['a']._value() == "2008-05-07"
    assert F['b'].data == d
    assert F['b']._value() == "05/07 2008"
    assert F['c'].data == d
    assert F['c']._value() == "5/7 2008"


def test_failure():
    F.process(DummyPostData(a=["2008-bb-cc"], b=["hi"]))
    assert not F.validate()
    assert len(F['a'].process_errors) == 1
    assert len(F['a'].errors) == 1
    assert len(F['b'].errors) == 1
    assert F['a'].process_errors[0] == "Not a valid date value."
