from tests.common import DummyPostData

from formful.fields import StringField
from formful.form import Form
from formful.schema import Schema


class Fields(Schema):
    a = StringField(default=" hello", filters=[lambda x: x.strip()])
    b = StringField(default="42", filters=[int, lambda x: -x])


def test_working():
    form = Form(fields=Fields)
    form.process()
    assert form['a'].data == "hello"
    assert form['b'].data == -42
    assert form.validate()


def test_failure():
    form = Form(fields=Fields)
    form.process(DummyPostData(a=["  foo bar  "], b=["hi"]))
    assert form['a'].data == "foo bar"
    assert form['b'].data == "hi"
    assert len(form['b'].process_errors) == 1
    assert not form.validate()


def test_extra():

    def filter_a(value):
        return value.strip()

    def filter_b(value):
        return -int(value)

    form = Form(
        fields={
            "a": StringField(default=" hello "),
            "b": StringField(default="42")
        },
        extra_filters={
            "a": [filter_a],
            "b": [filter_b]
        }
    )
    form.process()
    assert "hello" == form['a'].data
    assert -42 == form['b'].data
    assert form.validate()
