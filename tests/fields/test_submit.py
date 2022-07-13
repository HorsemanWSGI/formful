from formful.fields import SubmitField
from formful.form import Form


def test_submit_field():
    assert Form(fields={
        'a': SubmitField("Label")
    }).fields['a']() == (
        """<input id="a" name="a" type="submit" value="Label">""")
