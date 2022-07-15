from formful import widgets
from formful.fields import PasswordField
from formful.form import Form
from formful.schema import Schema


class Fields(Schema):
    a = PasswordField(
        widget=widgets.PasswordInput(hide_value=False),
        default="LE DEFAULT"
    )
    b = PasswordField(default="Hai")


def test_password_field():
    form = Form(fields=Fields)
    form.process()
    assert form['a']() == (
        """<input id="a" name="a" type="password" value="LE DEFAULT">"""
    )
    assert form['b']() == (
        """<input id="b" name="b" type="password" value="">"""
    )
