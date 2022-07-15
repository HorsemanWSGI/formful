from tests.common import DummyPostData

from formful.fields import FloatField
from formful.form import Form
from formful.schema import Schema


class Fields(Schema):
    a = FloatField()
    b = FloatField(default=48.0)


def test_float_field():
    form = Form(fields=Fields)

    form.process(DummyPostData(a=["v"], b=["-15.0"]))
    assert form['a'].data is None
    assert form['a'].raw_data == ["v"]
    assert form['a']() == (
        """<input id="a" name="a" type="text" value="v">"""
    )
    assert form['b'].data == -15.0
    assert form['b']() == (
        """<input id="b" name="b" type="text" value="-15.0">"""
    )
    assert not form['a'].validate(form)
    assert form['b'].validate(form)

    form.process(DummyPostData(a=[], b=[""]))
    assert form['a'].data is None
    assert form['a']._value() == ""
    assert form['b'].data is None
    assert form['b'].raw_data == [""]
    assert not form.validate()
    assert len(form['b'].process_errors) == 1
    assert len(form['b'].errors) == 1

    form.process(b=9.0)
    assert form['b'].data == 9.0
    assert form['b']._value() == "9.0"
