from tests.common import DummyPostData

from formful.fields import FileField
from formful.fields import MultipleFileField
from formful.form import Form
from formful.widgets import TextInput


def test_file_field():
    class F(Form):
        file = FileField()

    assert F(DummyPostData(file=["test.txt"])).file.data == "test.txt"
    assert F(DummyPostData()).file.data is None
    assert F(DummyPostData(file=["test.txt", "multiple.txt"])).file.data == "test.txt"


def test_multiple_file_field():
    class F(Form):
        files = MultipleFileField()

    assert F(DummyPostData(files=["test.txt"])).files.data == ["test.txt"]
    assert F(DummyPostData()).files.data == []
    assert F(DummyPostData(files=["test.txt", "multiple.txt"])).files.data == [
        "test.txt",
        "multiple.txt",
    ]


def test_file_field_without_file_input():
    class F(Form):
        file = FileField(widget=TextInput())

    f = F(DummyPostData(file=["test.txt"]))
    assert f.file.data == "test.txt"
    assert f.file() == '<input id="file" name="file" type="text">'
