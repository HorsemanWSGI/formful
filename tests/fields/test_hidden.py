from formful.fields import HiddenField
from formful.form import Form


def test_hidden_field():
    form = Form(fields={
        'a': HiddenField(default="LE DEFAULT")
    })
    form.process()
    assert form['a']() == (
        """<input id="a" name="a" type="hidden" value="LE DEFAULT">"""
    )
    assert form['a'].flags.hidden
