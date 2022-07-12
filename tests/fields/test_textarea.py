from formful.fields import TextAreaField
from formful.form import Form


def test_textarea_field():
    form = Form(
        fields={"a": TextAreaField(default="LE DEFAULT")}
    )
    form.process()
    assert form.fields['a']() == (
        """<textarea id="a" name="a">\r\nLE DEFAULT</textarea>"""
    )
