from tests.common import DummyPostData

from formful import validators
from formful.fields import RadioField
from formful.form import Form
from formful.schema import Schema


class MySchema(Schema):
    a = RadioField(choices=[("a", "hello"), ("b", "bye")], default="a")
    b = RadioField(choices=[(1, "Item 1"), (2, "Item 2")], coerce=int)
    c = RadioField(
        choices=[("a", "Item 1"), ("b", "Item 2")],
        validators=[validators.InputRequired()],
    )


def test_radio_field():
    form = Form(fields=MySchema)
    form.process()
    assert form['a'].data == "a"
    assert form['b'].data is None
    assert form.validate() is False
    assert form['a']() == (
        '<ul id="a">'
        '<li><input checked id="a-0" name="a" type="radio" value="a"> '
        '<label for="a-0">hello</label></li>'
        '<li><input id="a-1" name="a" type="radio" value="b"> '
        '<label for="a-1">bye</label></li>'
        "</ul>"
    )
    assert form['b']() == (
        '<ul id="b">'
        '<li><input id="b-0" name="b" type="radio" value="1"> '
        '<label for="b-0">Item 1</label></li>'
        '<li><input id="b-1" name="b" type="radio" value="2"> '
        '<label for="b-1">Item 2</label></li>'
        "</ul>"
    )
    assert [str(x) for x in form['a']] == [
        '<input checked id="a-0" name="a" type="radio" value="a">',
        '<input id="a-1" name="a" type="radio" value="b">',
    ]


def test_text_coercion():
    # Regression test for text coercion scenarios where the value is a boolean.
    form = F(fields={
        'a': RadioField(
            choices=[(True, "yes"), (False, "no")],
            coerce=lambda x: False if x == "False" else bool(x),
        )
    })
    form.process()
    assert form['a']() == (
        '<ul id="a">'
        '<li><input id="a-0" name="a" type="radio" value="True"> '
        '<label for="a-0">yes</label></li>'
        '<li><input id="a-1" name="a" type="radio" value="False"> '
        '<label for="a-1">no</label></li>'
        "</ul>"
    )


def test_callable_choices():

    def choices():
        return [("a", "hello"), ("b", "bye")]

    form = Form(fields={
        'a': RadioField(choices=choices, default="a")
    })

    form.process()
    assert form['a'].data == "a"
    assert form['a']() == (
        '<ul id="a">'
        '<li><input checked id="a-0" name="a" type="radio" value="a"> '
        '<label for="a-0">hello</label></li>'
        '<li><input id="a-1" name="a" type="radio" value="b"> '
        '<label for="a-1">bye</label></li>'
        "</ul>"
    )


def test_required_flag():
    form = Form(fields=MySchema)
    form.process()
    assert form['c']() == (
        '<ul id="c">'
        '<li><input id="c-0" name="c" required type="radio" value="a"> '
        '<label for="c-0">Item 1</label></li>'
        '<li><input id="c-1" name="c" required type="radio" value="b"> '
        '<label for="c-1">Item 2</label></li>'
        "</ul>"
    )


def test_required_validator():
    form = Form(fields=MySchema)

    form.process(DummyPostData(b=1, c="a"))
    assert form.validate()
    assert form['c'].errors == []

    form.process(DummyPostData(b=1))
    assert form.validate() is False
    assert form['c'].errors == ["This field is required."]


def test_render_kw_preserved():
    form = Form(fields={
        'a': RadioField(
            choices=[(True, "yes"), (False, "no")],
            render_kw=dict(disabled=True)
        )
    })
    form.process()
    assert form['a']() == (
        '<ul disabled id="a">'
        '<li><input disabled id="a-0" name="a" type="radio" value="True"> '
        '<label for="a-0">yes</label></li><li>'
        '<input disabled id="a-1" name="a" type="radio" value="False"> '
        '<label for="a-1">no</label></li></ul>'
    )
