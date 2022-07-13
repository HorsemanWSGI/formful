from tests.common import DummyPostData
from formful.fields import StringField
from formful.form import Form


def test_string_field():
    form = Form(fields={
        'a': StringField()
    })
    form.process()
    assert form['a'].data is None
    assert form['a']() == """<input id="a" name="a" type="text" value="">"""
    form.process(DummyPostData(a=["hello"]))
    assert form['a'].data == "hello"
    assert form['a']() == (
        """<input id="a" name="a" type="text" value="hello">""")
    form.process(DummyPostData(b=["hello"]))
    assert form['a'].data is None
