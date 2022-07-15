import pytest
from tests.common import DummyPostData

from formful import validators
from formful import widgets
from formful.fields import SelectField
from formful.form import Form
from formful.schema import Schema


def test_select_field_copies_choices():

    fields = {
        'items': SelectField(choices=[])
    }
    f1 = Form(fields=fields)
    f2 = Form(fields=fields)

    f1['items'].choices.append(("a", "a"))
    f2['items'].choices.append(("b", "b"))

    assert f1['items'].choices == [("a", "a")]
    assert f2['items'].choices == [("b", "b")]
    assert f1['items'].choices is not f2['items'].choices


class MySchema(Schema):

    a = SelectField(
        choices=[("a", "hello"), ("btest", "bye")],
        default="a"
    )
    b = SelectField(
        choices=[(1, "Item 1"), (2, "Item 2")],
        coerce=int,
        option_widget=widgets.TextInput(),
    )


def test_defaults():
    form = Form(fields=MySchema)
    form.process()
    assert form['a'].data == "a"
    assert form['b'].data is None
    assert form.validate() is False
    assert form['a']() == (
        '<select id="a" name="a"><option selected value="a">hello</option>'
        '<option value="btest">bye</option></select>'
    )
    assert form['b']() == (
        '<select id="b" name="b"><option value="1">Item 1</option>'
        '<option value="2">Item 2</option></select>'
    )


def test_with_data():
    form = Form(fields=MySchema)
    form.process(DummyPostData(a=["btest"]))
    assert form['a'].data == "btest"
    assert form['a']() == (
        '<select id="a" name="a"><option value="a">hello</option>'
        '<option selected value="btest">bye</option></select>'
    )


def test_value_coercion():
    form = Form(fields=MySchema)
    form.process(DummyPostData(b=["2"]))
    assert form['b'].data == 2
    assert form['b'].validate(form)
    form.process(DummyPostData(b=["b"]))
    assert form['b'].data is None
    assert not form['b'].validate(form)


def test_iterable_options():
    form = Form(fields=MySchema)
    form.process()
    first_option = list(form['a'])[0]
    assert isinstance(first_option, form['a']._Option)
    assert list(str(x) for x in form['a']) == [
        '<option selected value="a">hello</option>',
        '<option value="btest">bye</option>',
    ]
    assert isinstance(first_option.widget, widgets.Option)
    assert isinstance(list(form['b'])[0].widget, widgets.TextInput)
    assert (
        first_option(disabled=True)
        == '<option disabled selected value="a">hello</option>'
    )


def test_default_coerce():
    form = Form(fields={
        "a": SelectField(choices=[("a", "Foo")])
    })
    form.process(DummyPostData(a=[]))
    assert not form.validate()
    assert form['a'].data is None
    assert len(form['a'].errors) == 1
    assert form['a'].errors[0] == "Not a valid choice."


def test_validate_choices():
    form = Form(fields={
        "a": SelectField(choices=[("a", "Foo")])
    })
    form.process(DummyPostData(a=["b"]))
    assert not form.validate()
    assert form['a'].data == "b"
    assert len(form['a'].errors) == 1
    assert form['a'].errors[0] == "Not a valid choice."


def test_validate_choices_when_empty():
    form = Form(fields={
        "a": SelectField(choices=[])
    })
    form.process(DummyPostData(a=["b"]))
    assert not form.validate()
    assert form['a'].data == "b"
    assert len(form['a'].errors) == 1
    assert form['a'].errors[0] == "Not a valid choice."


def test_validate_choices_when_none():
    form = Form(fields={
        "a": SelectField()
    })
    form.process(DummyPostData(a=["b"]))
    with pytest.raises(TypeError, match="Choices cannot be None"):
        form.validate()


def test_dont_validate_choices():
    form = Form(fields={
        "a": SelectField(choices=[("a", "Foo")], validate_choice=False)
    })
    form.process(DummyPostData(a=["b"]))
    assert form.validate()
    assert form['a'].data == "b"
    assert len(form['a'].errors) == 0


def test_choice_shortcut():
    form = Form(fields={
        "a": SelectField(choices=[("foo", "Foo")], validate_choice=False)
    })
    form.process(a="bar")
    assert '<option value="foo">foo</option>' in form['a']()


def test_choice_shortcut_post():
    form = Form(fields={
        "a": SelectField(choices=["foo", "bar"])
    })
    form.process(DummyPostData(a=["foo"]))
    assert form.validate()
    assert form['a'].data == "foo"
    assert len(form['a'].errors) == 0


@pytest.mark.parametrize("choices", [[], None, {}])
def test_empty_choice(choices):
    form = Form(fields={
        "a": SelectField(choices=choices, validate_choice=False)
    })
    form.process(a="bar")
    assert form['a']() == '<select id="a" name="a"></select>'


def test_callable_choices():
    def choices():
        return ["foo", "bar"]

    form = Form(fields={
        "a": SelectField(choices=choices)
    })
    form.process(a="bar")
    assert list(str(x) for x in form['a']) == [
        '<option value="foo">foo</option>',
        '<option selected value="bar">bar</option>',
    ]


def test_required_flag():

    form = Form(fields={
        "c": SelectField(
            choices=[("a", "hello"), ("b", "bye")],
            validators=[validators.InputRequired()]
        )
    })
    form.process(DummyPostData(c="a"))
    assert form['c']() == (
        '<select id="c" name="c" required>'
        '<option selected value="a">hello</option>'
        '<option value="b">bye</option>'
        "</select>"
    )


def test_required_validator():

    form = Form(fields={
        "c": SelectField(
            choices=[("a", "hello"), ("b", "bye")],
            validators=[validators.InputRequired()]
        )
    })
    form.process(DummyPostData(c="b"))
    assert form.validate()
    assert form['c'].errors == []

    form.process()
    assert form.validate() is False
    assert form['c'].errors == ["This field is required."]


def test_render_kw_preserved():
    form = Form(fields={
        'a': SelectField(
            choices=[("foo"), ("bar")],
            render_kw=dict(disabled=True))
    })
    form.process()
    assert form['a']() == (
        '<select disabled id="a" name="a">'
        '<option value="foo">foo</option>'
        '<option value="bar">bar</option>'
        "</select>"
    )


def test_optgroup():
    form = Form(fields={
        'a': SelectField(choices={"hello": [("a", "Foo")]})
    })
    form.process(a="a")
    assert (
        '<optgroup label="hello">'
        '<option selected value="a">Foo</option>'
        "</optgroup>" in form['a']()
    )
    assert list(form['a'].iter_choices()) == [("a", "Foo", True)]


def test_optgroup_shortcut():
    form = Form(fields={
        'a': SelectField(choices={"hello": ["foo", "bar"]})
    })
    form.process(a="bar")
    assert (
        '<optgroup label="hello">'
        '<option value="foo">foo</option>'
        '<option selected value="bar">bar</option>'
        "</optgroup>" in form['a']()
    )
    assert list(form['a'].iter_choices()) == [
        ("foo", "foo", False),
        ("bar", "bar", True)
    ]


@pytest.mark.parametrize("choices", [[], ()])
def test_empty_optgroup(choices):
    form = Form(fields={
        'a': SelectField(choices={"hello": choices})
    })
    form.process(a="bar")
    assert '<optgroup label="hello"></optgroup>' in form['a']()
    assert list(form['a'].iter_choices()) == []
