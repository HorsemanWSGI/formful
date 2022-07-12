import pytest
from tests.common import DummyPostData

from formful import validators
from formful.fields import SelectField
from formful.fields import SelectMultipleField
from formful.form import Form


def make_form(**fields):
    return Form(fields)


schema = dict(
    a = SelectMultipleField(
        choices=[("a", "hello"), ("b", "bye"), ("c", "something")], default=("a",)
    ),
    b = SelectMultipleField(
        coerce=int, choices=[(1, "A"), (2, "B"), (3, "C")], default=("1", "3")
    )
)


def test_defaults():
    form = Form(schema)
    assert form.a.data == ["a"]
    assert form.b.data == [1, 3]
    # Test for possible regression with null data
    form.a.data = None
    assert form.validate()
    assert list(form.a.iter_choices()) == [(v, l, False) for v, l in form.a.choices]


def test_with_data():
    form = Form(schema)
    form.process(DummyPostData(a=["a", "c"]))
    assert form.a.data == ["a", "c"]
    assert list(form.a.iter_choices()) == [
        ("a", "hello", True),
        ("b", "bye", False),
        ("c", "something", True),
    ]
    assert form.b.data == []
    form = F(DummyPostData(b=["1", "2"]))
    assert form.b.data == [1, 2]
    assert form.validate()
    form = F(DummyPostData(b=["1", "2", "4"]))
    assert form.b.data == [1, 2, 4]
    assert not form.validate()


def test_coerce_fail():
    form = Form(schema)
    form = form.process(b=["a"])
    assert form.validate()
    assert form.b.data is None
    form = F(DummyPostData(b=["fake"]))
    assert not form.validate()
    assert form.b.data == [1, 3]


def test_callable_choices():
    def choices():
        return ["foo", "bar"]

    F = make_form(a=SelectField(choices=choices))
    form = F(a="bar")

    assert list(str(x) for x in form.a) == [
        '<option value="foo">foo</option>',
        '<option selected value="bar">bar</option>',
    ]


def test_choice_shortcut():
    F = make_form(a=SelectMultipleField(choices=["foo", "bar"]))
    form = F(a=["bar"])
    assert form.validate()
    assert '<option value="foo">foo</option>' in form.a()


@pytest.mark.parametrize("choices", [[], None])
def test_empty_choice(choices):
    F = make_form(a=SelectMultipleField(choices=choices))
    form = F(a="bar")
    assert form.a() == '<select id="a" multiple name="a"></select>'


def test_validate_choices_when_empty():
    F = make_form(a=SelectMultipleField(choices=[]))
    form = F(DummyPostData(a=["b"]))
    assert not form.validate()
    assert form.a.data == ["b"]
    assert len(form.a.errors) == 1
    assert form.a.errors[0] == "'b' is not a valid choice for this field."


def test_validate_choices_when_none():
    F = make_form(a=SelectMultipleField())
    form = F(DummyPostData(a="b"))
    with pytest.raises(TypeError, match="Choices cannot be None"):
        form.validate()


def test_dont_validate_choices():
    F = make_form(a=SelectMultipleField(choices=[("a", "Foo")], validate_choice=False))
    form = F(DummyPostData(a=["b"]))
    assert form.validate()
    assert form.a.data == ["b"]
    assert len(form.a.errors) == 0


def test_requried_flag():
    F = make_form(
        c=SelectMultipleField(
            choices=[("a", "hello"), ("b", "bye")],
            validators=[validators.InputRequired()],
        )
    )
    form = F(DummyPostData(c=["a"]))
    assert form.c() == (
        '<select id="c" multiple name="c" required>'
        '<option selected value="a">hello</option>'
        '<option value="b">bye</option>'
        "</select>"
    )


def test_required_validator():
    F = make_form(
        c=SelectMultipleField(
            choices=[("a", "hello"), ("b", "bye")],
            validators=[validators.InputRequired()],
        )
    )
    form = F(DummyPostData(c=["a"]))
    assert form.validate()
    assert form.c.errors == []
    form = F()
    assert form.validate() is False
    assert form.c.errors == ["This field is required."]


def test_render_kw_preserved():
    F = make_form(
        a=SelectMultipleField(choices=[("foo"), ("bar")], render_kw=dict(disabled=True))
    )
    form = F()
    assert form.a() == (
        '<select disabled id="a" multiple name="a">'
        '<option value="foo">foo</option>'
        '<option value="bar">bar</option>'
        "</select>"
    )
