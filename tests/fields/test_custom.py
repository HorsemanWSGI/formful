import pytest

from formful.fields import SelectFieldBase
from formful.fields import StringField
from formful.form import Form


class MyCustomField(StringField):
    def process_data(self, data):
        if data == "fail":
            raise ValueError("Contrived Failure")

        return super().process_data(data)


class F(Form):
    a = MyCustomField()
    b = SelectFieldBase()


def test_processing_failure():
    form = F(a="42")
    assert form.validate()
    form = F(a="fail")
    assert not form.validate()


def test_default_impls():
    f = F()
    with pytest.raises(NotImplementedError):
        f.b.iter_choices()
