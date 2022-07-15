import pytest
from formful.fields import SelectFieldBase
from formful.fields import StringField
from formful.form import Form


class MyCustomField(StringField):
    def process_data(self, data):
        if data == "fail":
            raise ValueError("Contrived Failure")

        return super().process_data(data)


F  = Form(fields={
    'a': MyCustomField(),
    'b': SelectFieldBase()
})


def test_processing_failure():
    F.process(a="42")
    assert F.validate()
    F.process(a="fail")
    assert not F.validate()


def test_default_impls():
    F.process()
    with pytest.raises(NotImplementedError):
        F['b'].iter_choices()
